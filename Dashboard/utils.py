import streamlit as st
import pandas as pd

@st.cache_data
def carregar_dados():
    #df = pd.read_csv('https://raw.githubusercontent.com/lucasfreirec/datascience/refs/heads/main/dataset.csv')
    df = pd.read_csv('./dataset.csv')
    
    df = df.drop(['tconst', 'IMDbLink', 'Title_IMDb_Link'], axis=1)

    df = df.fillna("Desconhecido")
    df['genres'] = df['genres'].str.split(',').str[0]

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