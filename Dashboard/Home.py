import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Dashboard: Top 5000 IMDb", page_icon="📝", layout="wide")



st.title('Top 5000 filmes do IMDb')

st.sidebar.image("./imgs/logo.jpg", width=150)

st.sidebar.title("CIÊNCIA DE DADOS")

st.sidebar.markdown("### Docente: <br> Luiz Affonso Henderson Guedes De Oliveira", unsafe_allow_html=True)
st.sidebar.markdown("### Discentes: <br> Ana Clara Fernandes Vieira <br> Lucas Freire Costa", unsafe_allow_html=True)

st.subheader('DESCRIÇÃO DO DASHBOARD')
st.text('Este dashboard ilustra análises realizadas sobre o dataset contendo ' \
'dados relacionados aos 5000 filmes mais bem rankeados pela plataforma de' \
' críticas e avaliações de cinema IMDb.')

st.header('ANÁLISE DAS NOTAS')
st.text('Analisando a coluna que diz respeito às notas dos filmes, foram encontradas ' \
'as seguintes relações: ')


