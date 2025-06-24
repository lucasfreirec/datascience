import streamlit as st
import pandas as pd

@st.cache_data
def carregar_dados():
    #df = pd.read_csv('https://raw.githubusercontent.com/lucasfreirec/datascience/refs/heads/main/dataset.csv')
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
        'Documentary': 'Documentário', 'Sport': 'Desporto', 'Musical': 'Musical',
        'Film-Noir': 'Film-Noir'
    }

    # Processa e traduz a coluna de géneros
    df['genres'] = df['genres'].str.split(',').str[0]
    df['genres'] = df['genres'].map(dicionario_generos).fillna(df['genres'])
    
    # Cria a coluna de diretor principal
    df['directors'] = df['directors'].str.split(',').str[0]

    return df

def classificar_periodo(ano):
    if 1920 <= ano <= 1939:
        return '1920-1939'
    elif 1940 <= ano <= 1959:
        return '1940-1959'
    elif 1960 <= ano <= 1979:
        return '1960-1979'
    elif 1980 <= ano <= 1999:
        return '1980-1999'
    elif 2000 <= ano <= 2020:
        return '2000-2020'
    else:
        return 'Fora do intervalo'
    
@st.cache_data
def preparar_dados_sunburst(df):
    """Prepara os dados para o gráfico Sunburst, usando colunas já processadas."""
    df_sunburst = df.copy()
    df_sunburst = df_sunburst[df_sunburst['directors'] != 'Desconhecido']
    df_sunburst = df_sunburst[df_sunburst['genres'] != 'Desconhecido']
    top_generos = df_sunburst['genres'].value_counts().nlargest(10).index
    df_filtrado = df_sunburst[df_sunburst['genres'].isin(top_generos)]
    return df_filtrado