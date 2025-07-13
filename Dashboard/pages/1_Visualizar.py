import streamlit as st
import pandas as pd
import plotly.express as px
from utils import *
import numpy as np

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

st.markdown("---")

st.title("Gráfico Sunburst")

df_para_grafico = preparar_dados_sunburst(df_imdb)

st.markdown("Clique nos anéis para se aprofundar nos dados. O tamanho da fatia representa a popularidade (votos) e a cor representa a qualidade (nota).")

fig = px.sunburst(
    df_para_grafico,
    path=['genres', 'directors', 'primaryTitle'], 
    values='numVotes',
    color='averageRating',
    color_continuous_scale='YlOrRd', 
    hover_data={'averageRating': ':.2f'},
    maxdepth=2 
)
fig.update_layout(margin=dict(t=10, l=10, r=10, b=10))
st.plotly_chart(fig, use_container_width=True, height=800)

st.markdown("---")
st.header("Qual Gênero Tem as Melhores Notas?")

media_por_genero = df_imdb.groupby('genres')['averageRating'].mean().sort_values(ascending=False).reset_index()

fig_barras = px.bar(
    media_por_genero.head(15), 
    x="averageRating",
    y="genres",
    orientation='h',
    title="Nota Média por Gênero Cinematográfico (Top 15)",
    text='averageRating'
)

fig_barras.update_traces(texttemplate='%{text:.2f}', textposition='outside')
fig_barras.update_layout(
    xaxis_title="Nota Média IMDb",
    yaxis_title="Gênero",
    uniformtext_minsize=8, 
    uniformtext_mode='hide',
    yaxis={'categoryorder':'total ascending'} 
)

st.plotly_chart(fig_barras, use_container_width=True)

st.markdown("---")

st.header("Mapa de Correlação")

df_numeric = df_imdb.select_dtypes(include=np.number)

corr_matrix = df_numeric.corr()

fig_heatmap = px.imshow(
    corr_matrix,
    text_auto=True, 
    aspect="auto",   
    color_continuous_scale='RdBu_r', 
    range_color=[-1, 1], 
    title="Matriz de Correlação"
)

fig_heatmap.update_layout(
    margin=dict(l=10, r=10, t=50, b=10),
)

st.plotly_chart(fig_heatmap, use_container_width=True)


