import streamlit as st
import pandas as pd
import plotly.express as px
from utils import *

st.set_page_config(page_title="Visualização", page_icon="./Dashboard/imgs/logo.jpg", layout="wide")

st.title("Visualização dos dados")

df_imdb = carregar_dados()

df_imdb['startYear'] = df_imdb['startYear'].apply(classificar_periodo)

st.write("### Escolha como visualizar os dados:")

opcoes_de_agrupamento = ['averageRating', 'genres', 'startYear']
opcao = st.selectbox(
    "Visualizar quantidades de:",
    options=opcoes_de_agrupamento
)

dados_para_plotar = df_imdb.groupby(opcao).size().reset_index(name='Quantidade')

st.write(f"### Gráfico de Quantidade por {opcao}")
fig = px.bar(
    dados_para_plotar,
    x=opcao,
    y='Quantidade',
    text_auto=True,
    color_discrete_sequence=['#FFC300']
)

st.plotly_chart(fig, use_container_width=True)