import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
from scipy.sparse import hstack

st.set_page_config(page_title="Recomendações de filmes", page_icon="./Dashboard/imgs/logo.jpg", layout="wide")


@st.cache_data
def carregar_dados_para_ml():
    """
    Função de carregamento de dados dedicada para a página de ML.
    Carrega o dataset, faz a limpeza inicial e adiciona uma coluna
    com o gênero principal traduzido para português.
    """
    df = pd.read_csv('./dataset.csv')
    df = df.drop(['tconst', 'IMDbLink', 'Title_IMDb_Link'], axis=1)
    df = df.fillna("Desconhecido")
    
    dicionario_generos = {
        'Drama': 'Drama', 'Action': 'Ação', 'Comedy': 'Comédia',
        'Crime': 'Crime', 'Biography': 'Biografia', 'Adventure': 'Aventura',
        'Animation': 'Animação', 'Horror': 'Terror', 'Mystery': 'Mistério',
        'Sci-Fi': 'Ficção Científica', 'Thriller': 'Suspense', 'Romance': 'Romance',
        'Fantasy': 'Fantasia', 'Family': 'Família', 'History': 'História',
        'War': 'Guerra', 'Music': 'Música', 'Western': 'Faroeste',
        'Documentary': 'Documentário', 'Sport': 'Esporte', 'Musical': 'Musical',
        'Film-Noir': 'Film-Noir'
    }
    
    df['genero_principal_en'] = df['genres'].str.split(',').str[0]
    
    df['genero_principal_pt'] = df['genero_principal_en'].map(dicionario_generos).fillna(df['genero_principal_en'])
    
    return df

@st.cache_resource
def treinar_modelo(df, text_weight):
    """
    Prepara os dados e calcula a matriz de similaridade.
    """
    df_copy = df.copy()
    
    df_copy['genres_processed'] = df_copy['genres'].str.replace(',', ' ')
    df_copy['directors_processed'] = df_copy['directors'].apply(
        lambda x: ' '.join(d.replace(' ', '') for d in str(x).split(','))
    )
    df_copy['text_features'] = df_copy['genres_processed'] + ' ' + df_copy['directors_processed']
    
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df_copy['text_features'])

    numeric_features = df_copy[['averageRating', 'numVotes', 'runtimeMinutes', 'startYear']].fillna(0)
    scaler = MinMaxScaler()
    numeric_scaled = scaler.fit_transform(numeric_features)

    combined_features = hstack([tfidf_matrix * text_weight, numeric_scaled * (1 - text_weight)])
    
    cosine_sim = cosine_similarity(combined_features, combined_features)
    
    return cosine_sim

df_original = carregar_dados_para_ml()
indices = pd.Series(df_original.index, index=df_original['primaryTitle']).drop_duplicates()

st.title("Encontre filmes parecidos com os que você já gosta")
st.markdown("""
A recomendação é baseada numa análise híbrida de cada filme, combinando todos os gêneros e diretores com nota, popularidade, ano e duração (Dados númericos).

**Nota sobre o modelo:** O algoritmo não analisa o enredo, ele é excelente a encontrar filmes com um estilo de direção e gênero semelhantes. No entanto, pode não identificar franquias diretas se o diretor for diferente, por exemplo.
""")
st.markdown("---")

st.sidebar.header("Configurações do Modelo")
peso_texto = st.sidebar.slider(
    "Peso para Gênero/Diretor vs. Dados Numéricos",
    min_value=0.0, max_value=1.0, value=0.7, step=0.05,
    help="100% = Apenas gênero/diretor. 0% = Apenas nota/votos/ano/duração."
)

matriz_similaridade = treinar_modelo(df_original, peso_texto)

st.header("Selecione um Filme para Obter Recomendações")

col_genero, col_ano = st.columns(2)
with col_genero:
    lista_generos_pt = sorted(df_original['genero_principal_pt'].unique())
    genero_filtro_pt = st.selectbox(
        "Filtre por Gênero:",
        options=["Todos"] + lista_generos_pt
    )
with col_ano:
    ano_filtro = st.slider(
        "Filtre por Ano de Lançamento:",
        min_value=int(df_original['startYear'].min()),
        max_value=int(df_original['startYear'].max()),
        value=(int(df_original['startYear'].min()), int(df_original['startYear'].max()))
    )

df_filtrado = df_original[
    (df_original['startYear'] >= ano_filtro[0]) & (df_original['startYear'] <= ano_filtro[1])
]
if genero_filtro_pt != "Todos":
    df_filtrado = df_filtrado[df_filtrado['genero_principal_pt'] == genero_filtro_pt]

titulo_filme = None

if not df_filtrado.empty:
    titulo_filme = st.selectbox(
        f"Selecione um filme da lista filtrada ({len(df_filtrado)} encontrados):",
        options=sorted(df_filtrado['primaryTitle'].unique())
    )
else:
    st.warning("Nenhum filme encontrado com os filtros selecionados.")

if titulo_filme:
    try:
        idx = indices[titulo_filme]
        sim_scores = list(enumerate(matriz_similaridade[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:6]
        movie_indices = [i[0] for i in sim_scores]
        filmes_recomendados = df_original.iloc[movie_indices]

        st.markdown("---")
        st.subheader(f"Porque você assistiu a **{titulo_filme}**, talvez goste de:")

        cols = st.columns(5)
        for i, row in enumerate(filmes_recomendados.iterrows()):
            filme = row[1]
            with cols[i]:
                st.markdown(f"**{filme['primaryTitle']}** ({int(filme['startYear'])})")
                st.markdown(f"**Nota:** {filme['averageRating']} ⭐")
                st.markdown(f"**Gênero:** {filme['genero_principal_pt']}")
                st.markdown(f"**Diretor:** {filme['directors'].split(',')[0]}")
                
                similarity_score = sim_scores[i][1]
                if similarity_score >= 0.90:
                    st.success(f"Similaridade: {similarity_score:.2%}")
                elif similarity_score >= 0.75:
                    st.warning(f"Similaridade: {similarity_score:.2%}")
                else:
                    st.error(f"Similaridade: {similarity_score:.2%}")

    except KeyError:
        st.error("Filme não encontrado. Por favor, tente outro.")
