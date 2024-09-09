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
        # Tratando dados do mindmap
        
        dados_df = pd.DataFrame(data, index=[0])
        dados_df = dados_df["texto"].str.split(r'(?<!\d)1\.',expand=True)
        dados_df = dados_df.transpose()
        dados_df = dados_df[0].str.replace("10.","").str.replace("9.","").str.replace("8.","").str.replace("7.","").str.replace("6.","").str.replace("5.","").str.replace("4.","").str.replace("3.","").str.replace("2.","").replace("1.","")
        
        # Transformando os dados do dataframe em lista
        i = 0
        range = len(dados_df)
        dados = []
        
        while i < range:
            if dados_df[i] != "":
                dados.append(dados_df[i])
                i += 1
            else:
                i += 1
        
        
        dados1 = []
        j = 0
        range2 = len(dados)
        print(range2)
        
        while j < range2:
            if dados[j].count('*') == 1:
                j += 1
            else:
                dados1.append(dados[j])
                j += 1
        
        # Separando e criando novas listas 
        k = 0
        dados2 = []
        dados3 = []
        
        range2 = len(dados1)
        
        while k < range2:
            if dados1[k].count('*') == 2:
                    dados3.append(dados1[k])
                    dados2.append("")
                    k +=1 
            else:
                    dados2.append(dados1[k])
                    dados3.append("")
                    k += 1
                    #print(f'{k}° tabela 2: {dados2}\n, tabela 3: {dados3}\n')


        df2 = pd.DataFrame(dados2)
        df3 = pd.DataFrame(dados3)
        
        df2
        df3

        w = 0
        dados4 = []
        
        while w < len(dados2):
            dados4.append(dados3[w])
            w += 1
            
        #df2 = pd.DataFrame(dados2)
        #df4 = pd.DataFrame(dados4)
        
        testes = pd.DataFrame({'Caso de teste':dados2,'Detalhes':dados3})
        testes