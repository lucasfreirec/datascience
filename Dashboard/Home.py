import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Top 5000 IMDb", page_icon="./Dashboard/imgs/logo.jpg", layout="wide")

st.title('Top 5000 filmes do IMDb')

st.sidebar.image("./Dashboard/imgs/logo.jpg", width=150)

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

