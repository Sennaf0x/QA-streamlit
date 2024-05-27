import streamlit as st
import pandas as pd
from openai import OpenAI
import json
import os

st.set_page_config(layout="wide")

# Inicialize o DataFrame na sessão

if 'df' not in st.session_state:
    try:
        st.session_state['df'] = pd.read_csv('dados.csv')
    except FileNotFoundError:
        st.session_state['df'] = pd.DataFrame(columns=["Teste", "Descrição", "Gherkin"])

def reset_dataframe():

    st.session_state['df'] = pd.DataFrame(columns=["Teste", "Descrição", "Gherkin"])
    if os.path.exists('dados.csv'):
        os.remove('dados.csv')

col1, col2 = st.columns(2)

st.markdown('''
                <style>
                *{
                    margin:0;
                    padding:0;
                    box-sizing: border-box;
                }
        
                .letra{
                    color:white;
                }
                
                .block-container{
                    background-color: #611C8F;
                }
                
                .flex{
                    display:flex;
                }
                
                .main-1{
                    display:flex;
                    height: 200px;
                    margin: 10px;
                }
                .main-2{
                    display:grid;
                    heoght: 200px;
                    margin: 15px;
                }
                
                .italic{
                    color:rgb(107, 106, 104);
                    font-style: italic;
                }
                

                .header{
                    border-radius: 10px;
                    background-color: #EE039C;
                    text-align: center;
                    color: white;
                    box-shadow: rgba(0, 0, 0, 0.1) 0px 4px 12px;
                }
        
                .center{
                    text-align: center;
                    box-shadow: rgba(0, 0, 0, 0.1) 0px 4px 12px;
                    border-radius: 10px 10px 0 0;
                    background-color: #EE039C;
                    color: white;
                    box-shadow: rgba(50, 50, 93, 0.25) 0px 6px 12px -2px, rgba(0, 0, 0, 0.3) 0px 3px 7px -3px;
                }
                
                .card{
                    margin: 10px;
                    border: solid 1px;
                    background-color: aliceblue;
                    width: 100%;
                    height: 100%;
                    border-radius: 10px;
                }
                .card-2{
                    margin: 10px auto;
                    border: solid 1px;
                    background-color: aliceblue;
                    height: 100%;
                    width: 99%;
                    border-radius: 10px;
                }
                
                .title{ 
                    font-size: 20px;
                    font-weight: bold;
                    border-bottom: solid 1px;
                    margin: auto;
                }
                
                .justify{
                    text-align: justify;
                    margin:10px;
                }
                .stButton{
                    text-align: center;
                }
                
                @media (max-width: 400px) {
                    .title{
                        font-size: 12px;
                    }
                }
                </style>
                ''', unsafe_allow_html=True)

client = OpenAI()

resposta = ''
mensagem = ''

def ask_openai(mensagem):
    if mensagem.strip() == "":
        return "Como posso ajudá-lo?"
    try:
        completion = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (f'''
                                    Reescreva o caso de teste e dê 3 exemplos como se fosse um analista da qualidade 
                                    de software sênior:
                                    Caso de teste: {mensagem}
                                '''
                                )
                },
                {
                    "role": "user",
                    "content": ('''
                                    1. Reescrever de maneira diferente e técnica o <caso>.\n
                                    2. Estipular o cenário de teste, de maneira resumida.\n
                                    3. Estipular os riscos atraledos.\n
                                    4. Os passos no padrão gherkin para o caso de teste submetido.\n
                                    5. Não exiba os caracteres de quebra de linha("\\n").\n\n
                                    Utilize o seguinte exemplo para exibir a resposta como se fosse um arquivo json:\n
                                    {
                                    "caso": "<caso>",
                                    "cenario": "<cenario>",
                                    "riscos": "<riscos>",
                                    "gherkin": "<gherkin>"
                                    }
                                '''

                        )

                }

            ],

            temperature=1,
            max_tokens=1000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0

            )
        
        answer = completion.choices[0].message.content
        resposta_json = json.loads(answer.replace('\\n', ''))
        return resposta_json
    
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON: {e}")
        return None

    except Exception as e:
        print(f"Erro inesperado: {e}")
        return None

with col1:
    with st.container():
        with st.form(key='revisar_casos_form'):
            st.write('''<h1 class="header">Reescreva os casos de testes</h1>''', unsafe_allow_html=True)
            mensagem = st.text_input("Digite aqui o caso de teste:", label_visibility="hidden", key="case")
            submit_button = st.form_submit_button(label='Submeter')

    if submit_button and mensagem:
        resposta = ask_openai(mensagem)
        if resposta:
            st.session_state['resposta'] = resposta
            with st.container():

                st.write(f'''
                            <div>
                                <div class="main-1">
                                    <div class="card">
                                        <div class="center">
                                            <p class="title">CASO DE TESTE</p>
                                        </div>
                                        <div class="justify">
                                            <p>{json.dumps(resposta["caso"], ensure_ascii=False)}</p>
                                        </div>
                                    </div>
                                    <div class="card">
                                        <div class="center">
                                            <p class="title">CENÁRIO DE TESTE</p>
                                        </div>
                                        <div class="justify">
                                            <p>{json.dumps(resposta["cenario"], ensure_ascii=False)}</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        ''', unsafe_allow_html=True)
                st.write(f'''
                    <div>
                        <div class="main-2">
                            <div class="card-2">
                                <div class="center">
                                    <p class="title">GHERKIN</p>
                                </div>
                                <div class="justify">
                                    <p>{json.dumps(resposta["gherkin"], ensure_ascii=False)}</p>
                                </div>
                            </div>
                            <div class="card-2">
                                <div class="center">
                                    <p class="title">RISCOS RELACIONADOS</p>
                                </div>
                                <div class="justify">
                                    <p>{json.dumps(resposta["riscos"], ensure_ascii=False)}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                ''', unsafe_allow_html=True)
                
    st.write('''<div class="header">
                    <p>Deseja manter ou modificar o caso de teste?</p>
                </div>
             ''',unsafe_allow_html=True)
    col3, col4 = st.columns(2)
    with col3:
        add = st.button("Adicionar", key="Adicionar")
        if add:

            if 'resposta' in st.session_state:
                resposta = st.session_state['resposta']
                df_new_row = pd.DataFrame({
                    "Teste": [mensagem],
                    "Descrição": [resposta["cenario"]],
                    "Gherkin": [resposta["gherkin"]]
                })
                st.session_state.df = pd.concat([st.session_state.df, df_new_row], ignore_index=True)
                st.session_state.df.to_csv('dados.csv', index=False)
    
    with col4:
        mod = st.button("Modificar", key="Modificar")
        if mod:
            if 'resposta' in st.session_state:
                resposta = st.session_state['resposta']
                df_new_row = pd.DataFrame({
                    "Teste": [resposta["caso"]],
                    "Descrição": [resposta["cenario"]],
                    "Gherkin": [resposta["gherkin"]]
                })
                st.session_state.df = pd.concat([st.session_state.df, df_new_row], ignore_index=True)
                st.session_state.df.to_csv('dados.csv', index=False)

with col2:
    with st.form(key="deletar"):
        with st.container():
            st.write('<h1 class="header">Área da tabela</h1>', unsafe_allow_html=True)
            st.dataframe(st.session_state.df)
        
        delete = st.form_submit_button(label="Deletar")
        if delete:
            st.session_state.df = st.session_state.df[0:0]
            st.experimental_rerun()