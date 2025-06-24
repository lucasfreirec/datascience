import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from utils import carregar_dados

st.set_page_config(
    page_title="Top 5000 IMDb", 
    page_icon="https://raw.githubusercontent.com/lucasfreirec/datascience/main/Dashboard/imgs/logo.jpg", 
    layout="wide"
)

st.sidebar.image("https://raw.githubusercontent.com/lucasfreirec/datascience/main/Dashboard/imgs/logo.jpg", width=150)
st.sidebar.title("DASHBOARD - CIÊNCIA DE DADOS")
st.sidebar.markdown("---")
st.sidebar.markdown("### Docente:")
st.sidebar.markdown("Luiz Affonso Henderson Guedes De Oliveira")
st.sidebar.markdown("### Discentes:")
st.sidebar.markdown("Ana Clara Fernandes Vieira <br> Lucas Freire Costa", unsafe_allow_html=True)


st.title('🎬 Análise dos Top 5000 Filmes do IMDb')
st.markdown("O IMDb (Internet Movie Database) é a maior enciclopédia online do mundo sobre cinema, TV e celebridades, servindo " \
"como uma referência global para informações detalhadas na área. Milhões de utilizadores contribuem com avaliações " \
"e críticas, tornando-o o principal destino para descobrir, avaliar e discutir entretenimento.")

df_imdb = carregar_dados()

st.markdown("---")
st.header('Estatísticas básicas do dataset')

total_filmes = len(df_imdb)
nota_media = df_imdb['averageRating'].mean()
ano_mais_recente = df_imdb['startYear'].max()

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total de filmes", f"{total_filmes:,}".replace(",", "."))
with col2:
    st.metric("Nota média geral", f"{nota_media:.2f} ⭐")
with col3:
    st.metric("Filme mais recente", f"{int(ano_mais_recente)}")

col4, col5, col6 = st.columns(3)
with col4:
    genero_mais_comum = df_imdb['genres'].mode()[0]
    st.metric("Gênero mais frequente", genero_mais_comum)
with col5:
    diretor_mais_prolifico = df_imdb[df_imdb['directors'] != 'Desconhecido']['directors'].mode()[0]
    st.metric("Diretor com mais filmes", diretor_mais_prolifico)
with col6:
    duracao_media = df_imdb['runtimeMinutes'].mean()
    st.metric("Duração média", f"{int(duracao_media)} min ⏳")

st.markdown("---")

st.image("https://raw.githubusercontent.com/lucasfreirec/datascience/main/Dashboard/imgs/home.png", use_container_width=True)


st.markdown("---")
st.header('Explore as Análises')

col_vis, col_pesq = st.columns(2)
with col_vis:
    st.subheader('Visualização de Dados')
    st.markdown('Acesse aqui a visão geral do perfil dos top 5000 filmes através de gráficos interativos.')
    st.page_link("pages/1_Visualização.py", label="**Ir para a página de visualização**", icon="➡️")
with col_pesq:
    st.subheader('Pesquisa Detalhada')
    st.markdown('Acesse aqui para realizar pesquisas por título, ano, diretor e outros filtros.')
    st.page_link("pages/2_Pesquisa.py", label="**Ir para a página de pesquisa**", icon="➡️")

