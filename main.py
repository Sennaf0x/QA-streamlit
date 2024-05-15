import streamlit as st
from openai import OpenAI
import json

st.set_page_config(layout="wide")

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
            
            .main{
                display:flex;
                margin: 10px;
            }
            .main-2{
                display:grid;
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
            
            @media (max-width: 400px) {
                .title{
                    font-size: 12px;
                }
            }
            
        </style>
            ''', unsafe_allow_html=True)

client = OpenAI()

def ask_openai(mensagem):
    
    if(mensagem == ""):
        resposta = "Como posso ajudá-lo?"
        return resposta
    
    else: 
        completion = client.chat.completions.create(
            model="gpt-4-turbo",
            
                messages=[
                        {
                            "role": "system",
                            "content": f''' 
                                        Reescreva o caso de teste e dê 3 exemplos como se fosse um analista da qualidade de software senior:

                                        Caso de teste: {mensagem}
                                       '''
                        },
                        {
                            "role": "user",
                            "content": '''
                                        1. Reescrever de maneria diferente e técnica o <caso de teste> enviado dando 3 opções e enumerando eles no no campo <caso>                                         
                                        2. Estipular o cenário de teste, de maneira resumida, e inseri-lo em <cenario>                                          
                                        3. Estipular os riscos atraledos em <riscos>                                        
                                        4. Os passos no padrão gherkin para o caso de teste submetido, inserido em <gherkin>                                     
                                        5. Não exiba os caracteres de quebra de linha(\n)                                          
                                        Utilize o seguinte exemplo para exibir a resposta como se fosse um arquivo json:                                          
                                            {                                         
                                                "caso": "<caso>",                                          
                                                "cenario":"<cenario>",
                                                "riscos": "<riscos>",                                          
                                                "gherkin":"<gherkin>"
                                            }
                                       '''
                    }
                ],
                temperature=1,
                max_tokens=1000,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
                )
            
        answer = completion.choices[0].message.content
        resposta_json = json.loads(answer)
        print("resposta json: ", resposta_json)
        return resposta_json



with col1:    
    with st.container():
        st.write('''
                <h1 class="header">Reescreva os casos de testes</h1>
                ''', unsafe_allow_html=True)
        mensagem = st.text_input("Digite aqui o caso de teste:", label_visibility="hidden")
        st.write('''
                <p class="letra">Digite aqui o caso de teste</p>
                ''',unsafe_allow_html=True)
        
        if (mensagem == ""):
                with st.container(height=150,border=None):   
                    st.write('''
                        <div>
                            <div class="main">
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
                            </div>
                        </div>''',unsafe_allow_html=True)
                with st.container(height=300):    
                    st.write('''
                        <div class="main-2">
                            <div class="card-2">    
                                <div class="center">
                                    <p class="title">GHERKIN</p>
                                </div>
                                <div class="justify italic">
                                    <p>Passos</p>
                                </div>
                            </div>               
                            <div class="card-2">    
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
            with st.container(height=275):
                st.write(f'''
                        <div>
                            <div class="main">
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
                                        <p class="title">CENÁRIO DE TESTE </p>
                                    </div>
                                    <div class="justify">
                                        <p>{json.dumps(resposta["cenario"], ensure_ascii=False)}</p>
                                    </div>
                                </div>
                            </div>
                        </div>''', unsafe_allow_html=True)
            with st.container(height=300):
                    st.write(f'''
                            <div> 
                                <div class="main-2">
                                    <div class="card-2">    
                                        <div class="center">
                                            <p class="title">GHERKIN</p>
                                        </div>
                                        <div class="justify">
                                            <p>{json.dumps(resposta['gherkin'], ensure_ascii=False)}</p>
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
                                    <div>               
                                </div>
                            </div>
                            
                        ''', unsafe_allow_html=True)
with col2:
    st.write('<h1 class="header">Área da tabela</h1>',unsafe_allow_html=True)        