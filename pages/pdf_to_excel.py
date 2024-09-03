import streamlit as st
import pandas as pd
from openai import OpenAI
import json

st.set_page_config(layout="wide")


dados = ""

with st.form(key='Texto para csv'):
    texto = st.text_input("Insira o texto abaixo:")
    data={'texto': f'{texto}'}        
    
    submit_button = st.form_submit_button(label='Submeter')
    if submit_button:
        dados_df = pd.DataFrame(data, index=[0])
        dados_df = dados_df["texto"].str.split("1.",expand=True)
        dados_df = dados_df.transpose()
        dados_df = dados_df[0].str.replace("10.","").str.replace("9.","").str.replace("8.","").str.replace("7.","").str.replace("6.","").str.replace("5.","").str.replace("4.","").str.replace("3.","").str.replace("2.","").str.replace("1.","")
        dados_df
        print(dados_df)
        
    