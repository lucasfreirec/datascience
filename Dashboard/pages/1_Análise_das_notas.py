import streamlit as st
import pandas as pd
import plotly.express as px
from utils import carregar_dados

df_imdb = carregar_dados()

st.title("🔎 Análise por Gênero")
st.markdown("Compare o desempenho e a popularidade dos diferentes gêneros cinematográficos.")

# === Seletores ===
st.header('Seletores')
col1, col2 = st.columns(2)

with col1:
    genero = st.selectbox(
        'Escolha um gênero',
        ['Todos'] + sorted(df_imdb['genres'].unique().tolist())
    )
    
    if genero != 'Todos':
        st.write(f'Dados do gênero {genero}:')
        st.dataframe(df_imdb[df_imdb['genres'] == genero], use_container_width=True)
    else:
        st.write('Mostrando todas aos gêneros')
    
    colunas_selecionadas = st.multiselect(
        'Selecione as colunas para visualizar',
        df_imdb.columns.tolist(),
        default=['primaryTitle', 'rank', 'averageRating']
    )
    if colunas_selecionadas:
        st.dataframe(df_imdb[colunas_selecionadas], use_container_width=True)

with col2:
    metrica = st.radio(
        'Escolha uma métrica para análise',
        ['Renda Mensal por Pessoa', 'Rendimento Nominal Médio', 'População']
    )
    
    if metrica == 'Renda Mensal por Pessoa':
        coluna = 'renda_mensal_pessoa'
        unidade = 'R$'
    elif metrica == 'Rendimento Nominal Médio':
        coluna = 'rendimento_nominal_medio'
        unidade = 'salários mínimos'
    else:
        coluna = 'populacao'
        unidade = 'habitantes'
    
    st.write(f'Estatísticas de {metrica}:')