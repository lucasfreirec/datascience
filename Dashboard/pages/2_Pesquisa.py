import streamlit as st
import pandas as pd
from utils import carregar_dados

st.set_page_config(page_title="Pesquisa", page_icon="./Dashboard/imgs/logo.jpg", layout="wide")

df_imdb = carregar_dados()

st.title("Ferramenta de Análise de Filmes")
st.markdown("Utilize os filtros abaixo para encontrar e analisar filmes por título, diretor, ano e nota.")

st.sidebar.header('Filtros de Pesquisa')

termo_pesquisa = st.sidebar.text_input(
    'Pesquisar por Título, Diretor ou Ano',
    help="Digite um termo e pressione Enter para buscar."
)

nota_min = float(df_imdb['averageRating'].min())
nota_max = float(df_imdb['averageRating'].max())

intervalo_notas = st.sidebar.slider(
    'Selecione o intervalo de notas (averageRating)',
    min_value=nota_min,
    max_value=nota_max,
    value=(nota_min, nota_max),
    step=0.1
)

df_filtrado = df_imdb.copy()

if termo_pesquisa:
    mask_titulo = df_filtrado['primaryTitle'].str.contains(termo_pesquisa, case=False, na=False)
    mask_diretor = df_filtrado['directors'].str.contains(termo_pesquisa, case=False, na=False)
    mask_ano = df_filtrado['startYear'].astype(str).str.contains(termo_pesquisa, case=False, na=False)
    df_filtrado = df_filtrado[mask_titulo | mask_diretor | mask_ano]

mask_notas = df_filtrado['averageRating'].between(intervalo_notas[0], intervalo_notas[1])
df_filtrado = df_filtrado[mask_notas]

st.header(f"Resultados da Pesquisa ({len(df_filtrado)} filmes encontrados)")

st.write("Selecione as colunas que deseja visualizar na tabela abaixo:")
colunas_disponiveis = df_imdb.columns.tolist()
colunas_selecionadas = st.multiselect(
    'Selecione as colunas',
    options=colunas_disponiveis,
    default=['rank', 'primaryTitle', 'directors', 'startYear', 'averageRating', 'genres'],
    label_visibility="collapsed"
)

if colunas_selecionadas:
    styled_df = (
        df_filtrado[colunas_selecionadas]
        .style
        .set_properties(**{'text-align': 'center'}) 
        .set_table_styles([{'selector': 'th', 'props': [('text-align', 'center')]}])
        .hide(axis="index")
    )
    
    st.dataframe(styled_df, use_container_width=True, height=500, hide_index=True)
else:
    st.warning("Por favor, selecione pelo menos uma coluna para visualizar os dados.")
