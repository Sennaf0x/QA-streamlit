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

if 'resposta' not in st.session_state:
    st.session_state.resposta = pd.DataFrame(columns=["Caso de tese", "Descrição", "Gherkin"])

    

def reset_dataframe():

    st.session_state['df'] = pd.DataFrame(columns=["Teste", "Descrição", "Gherkin"])
    if os.path.exists('dados.csv'):
        os.remove('dados.csv')

col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

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
                    font-size: 25px;
                    border-radius: 10px;
                    background-color: #EE039C;
                    text-align: center;
                    color: white;
                    box-shadow: rgba(0, 0, 0, 0.1) 0px 4px 12px;
                }

                .mag{
                    margin: 15px auto;
                }
                
                .mag-auto{
                    display: flex;
                    justify-content: center; 
                    align-items: center;
                    width: 100%; 
                    margin: 0px auto;
                }
                .imagem{
                    border-radius: 15px;
                    border: solid 2px #EE039C;
                    box-shadow: rgba(0, 0, 0, 0.16) 0px 4px 7px, #EE039C 0px 3px 6px;
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
    if mensagem == "":
        return "Como posso ajudá-lo?"
    try:
        print("Iniciando chat")
        completion = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {
                    "role": "system",
                    "content": ('''
                                    Você é um analista da qualidade senior que analisa um dataframe e cria descrições e o gherkin de cada caso de teste.
                                '''
                                )
                },
                {
                    "role": "user",
                    "content": (f'''
                                    Leia os casos de teste da planilha {mensagem} e crie novas colunas.
                                    'casos de teste' = utilizar o mesmo caso de teste da planilha. 
                                    'descrição' = Estipular o cenário de teste, de maneira resumida.
                                    'gherkin' = Os passos no padrão gherkin para o caso de teste submetido.
                                    Utilize o seguinte exemplo para exibir a resposta como se fosse um arquivo json:
                                    ['<caso de teste>':'casos de teste','<descrição>':'descrição','<gherkin>':'gherkin']
                                ''')
                }
            ],

            temperature=1,
            max_tokens=4000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0

            )
        
        answer = completion.choices[0].message.content
        print(f"answer: {answer}")
        #resposta_json = json.dumps(answer, ensure_ascii=False)
        #print(f"resposta_json: {resposta_json}")
        return answer
    
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON: {e}")
        return None

    except Exception as e:
        print(f"Erro inesperado: {e}")
        return None

with col1:
    with st.container():
        with st.form(key='revisar_casos_form'):
            st.write('''<h1 class="header">Faça o upload dos casos de testes</h1>''', unsafe_allow_html=True)
            dados = st.file_uploader("Insira o arquivo aqui:", type=["xlsx"])
            
            submit_button = st.form_submit_button(label='Submeter')

        if submit_button:
            df = pd.read_excel(dados)
            st.dataframe(df)
            json_df = df.to_json(orient='records',force_ascii=False,lines=True)
            resposta = ask_openai(json_df)
            resposta = resposta.replace('<','').replace('>','').strip()
            st.session_state.resposta = resposta
            print(f"Resposta do chat: {st.session_state.resposta}")
            #json_resposta = json.loads(resposta).replace('\n','').replace('[','').replace(']','')
            #print(f"json_resposta: {json_resposta}")
            
with col2:
    with st.container():
        if resposta == '':
            img_path = "https://ibb.co/WgDQ1Fb"
            st.write('''<h1 class="header mag">Planilha preenchida</h1>
                        <div class="mag-auto" >
                            <img class ="imagem" src="https://i.ibb.co/MM8bLpY/sem-planilha.png" alt="sem-planilha" border="0" />
                        </div>
                    ''', unsafe_allow_html=True)
        else:
            st.write('''<h1 class="header mag">Planilha preenchida</h1>
                    ''', unsafe_allow_html=True)
            df_novo = pd.read_json(st.session_state.resposta)
            st.dataframe(df_novo)      