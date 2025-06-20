import streamlit as st
import pandas as pd

@st.cache_data
def carregar_dados():
    #df = pd.read_csv('https://raw.githubusercontent.com/lucasfreirec/datascience/refs/heads/main/dataset.csv')
    df = pd.read_csv('/home/lucas/Projects/datascience/dataset.csv')
    
    df = df.drop(['tconst', 'IMDbLink', 'Title_IMDb_Link'], axis=1)

    df = df.fillna("Desconhecido")
    df['genres'] = df['genres'].str.split(',').str[0]

    return df