import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from utils import *

st.set_page_config(page_title="Top 5000 IMDb", page_icon="https://raw.githubusercontent.com/lucasfreirec/datascience/refs/heads/main/Dashboard/imgs/logo.jpg", layout="wide")

st.title('Top 5000 filmes do IMDb')

st.sidebar.image("https://raw.githubusercontent.com/lucasfreirec/datascience/refs/heads/main/Dashboard/imgs/logo.jpg", width=150)

st.sidebar.title("DASHBOARD - CIÊNCIA DE DADOS")

st.sidebar.markdown("### Docente: <br> Luiz Affonso Henderson Guedes De Oliveira", unsafe_allow_html=True)
st.sidebar.markdown("### Discentes: <br> Ana Clara Fernandes Vieira <br> Lucas Freire Costa", unsafe_allow_html=True)

st.header('Visualização dos dados')
st.subheader('Acesse aqui a visão geral do perfil dos top 5000 filmes.')
st.page_link("./pages/1_Visualização.py", label="**Ir para a página de visualização**", icon="➡️")

st.header('Pesquisa de filmes')
st.subheader('Acesse aqui para realizar pesquisas por título, ano de lançamento, diretor e outros.')
st.page_link("./pages/2_Pesquisa.py", label="**Ir para a página de pesquisa**", icon="➡️")

st.image("./Dashboard/imgs/home.png")

@st.cache_data
def preparar_dados_sunburst(df):
    """Prepara os dados para o gráfico Sunburst, tratando hierarquias."""
    # Fazer uma cópia para evitar alterar o dataframe original
    df_sunburst = df.copy()
    
    # Lidar com múltiplos diretores e géneros (vamos pegar apenas o primeiro de cada para simplificar a hierarquia)
    df_sunburst['diretor_principal'] = df_sunburst['directors'].str.split(',').str[0]
    df_sunburst['genero_principal'] = df_sunburst['genres'].str.split(',').str[0]
    
    # Remover entradas onde não temos diretor ou género
    df_sunburst = df_sunburst[df_sunburst['diretor_principal'] != 'Desconhecido']
    df_sunburst = df_sunburst[df_sunburst['genero_principal'] != 'Desconhecido']

    # Para manter o gráfico legível, vamos focar nos géneros mais populares
    top_generos = df_sunburst['genero_principal'].value_counts().nlargest(10).index
    df_filtrado = df_sunburst[df_sunburst['genero_principal'].isin(top_generos)]

    return df_filtrado

# Carregar os dados
df_imdb = carregar_dados()
df_para_grafico = preparar_dados_sunburst(df_imdb)


st.title("Gráfico Sunburst")
st.markdown("Clique nos anéis para se aprofundar nos dados. O tamanho da fatia representa a popularidade (pela quantidade de votos) e a cor representa a qualidade (nota).")


# Criar a figura do Sunburst
fig = px.sunburst(
    df_para_grafico,
    # Define a hierarquia: o caminho desde o centro até a borda
    path=['genero_principal', 'diretor_principal', 'primaryTitle'], 
    
    # O tamanho de cada fatia será proporcional ao número de votos
    values='numVotes',
    
    # A cor de cada fatia será baseada na nota média
    color='averageRating',
    
    # Define a escala de cores (amarelo para notas altas, escuro para baixas) - CORRIGIDO
    color_continuous_scale='YlOrRd', 
    
    # Texto que aparece ao passar o rato por cima
    hover_data={'averageRating': ':.2f'},
    
    # Limita a profundidade inicial do gráfico para não ficar muito poluído
    maxdepth=2 
)

# Ajustes finos no layout para um visual mais limpo e informativo
fig.update_layout(
    margin=dict(t=10, l=10, r=10, b=10)
)

# Renderiza o gráfico no Streamlit
st.plotly_chart(fig, use_container_width=True, height=800)