import streamlit as st
from openai import OpenAI
import json


st.markdown('''
        <style>
            .flex{
                display:flex;
            }

            .italic{
                color:rgb(107, 106, 104);
                font-style: italic;
            }

            .header{
                border-radius: 10px;
                background-color: blueviolet;
                text-align: center;
                color: white;
                box-shadow: rgba(0, 0, 0, 0.1) 0px 4px 12px;
            }

            .center{
                text-align: center;
                box-shadow: rgba(0, 0, 0, 0.1) 0px 4px 12px;
                background-color: blueviolet;
                color: white;
            }

            .card{
                margin: 10px;
                border: solid 1px;
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
        </style>
            ''')

client = OpenAI()

def ask_openai(mensagem):
    
    if(mensagem == ""):
        resposta = "Como posso ajudá-lo?"
        return resposta
    
    else: 
        completion = client.chat.completions.create(
            model="ft:gpt-3.5-turbo-0613:personal:cb-etech:8ZwbruP2",
            
                messages=[
                    {
                    "role": "system",
                    "content": ''' 
                                Você é um analista de QA e irá reescrever o caso de teste no campo <caso>, qual seria o cenário de teste, de maneira resumida, em <cenario> e o risco atraledos em <riscos> utilizando o seguinte exemplo como se fosse um arquivo json: 
                                {
                                 "caso": "<caso>",
                                 "cenario":"<cenario>",
                                 "riscos": "<riscos>"
                                }
                               '''},
                    {
                    "role": "user",
                    "content": mensagem
                    }
                ],
                temperature=1,
                max_tokens=200,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
                )
            
        answer = completion.choices[0].message.content
        resposta_json = json.loads(answer)
        print("resposta json: ", resposta_json)
        return resposta_json


with st.container():
    
    st.write('''
             <h1 class="header">Reescreva os casos de testes</h1>
             ''', unsafe_allow_html=True)
    mensagem = st.text_input("Digite aqui o caso de teste:")
    if (mensagem == ""):
        st.write('''
                <div>
                    <div class="card">
                        <div class="center">
                            <p class="title">CASO DE TESTE</p>
                        </div>
                        <div class="justify italic">
                            <p>Caso de teste reescrito...</p>
                        </div>
                    </div>
                    <div class="card">
                        <div class="center">
                            <p class="title">CENÁRIO DE TESTE </p>
                        </div>
                        <div class="justify italic">
                            <p>Cenário de teste...</p>
                        </div>
                    </div>
                    <div class="card">    
                        <div class="center">
                            <p class="title">RISCOS RELACIONADOS</p>
                        </div>
                        <div class="justify italic">
                            <p>Risco relacionado...</p>
                        </div>
                    </div>               
                </div>   
                ''', unsafe_allow_html=True)
    else:
        resposta = ask_openai(mensagem)

        with st.container():
            st.write(f'''
                    <div class="card">
                        <div>
                            <div class="center">
                                <p class="title">CASO DE TESTE</p>
                            </div>
                            <div class="justify">
                                <p>{json.dumps(resposta["caso"], ensure_ascii=False)}</p>
                            </div>
                        </div>
                        <div>
                            <div class="center">
                                <p class="title">CENÁRIO DE TESTE </p>
                            </div>
                            <div class="justify">
                                <p>{json.dumps(resposta["cenario"], ensure_ascii=False)}</p>
                            </div>
                        </div>
                        <div>    
                            <div class="center">
                                <p class="title">RISCOS RELACIONADOS</p>
                            </div>
                            <div class="justify">
                                <p>{json.dumps(resposta["riscos"], ensure_ascii=False)}</p>
                            </div>
                        </div>               
                    </div>   
                    ''', unsafe_allow_html=True)