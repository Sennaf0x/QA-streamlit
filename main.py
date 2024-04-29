import streamlit as st
from openai import OpenAI
import json

with open("style.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

client = OpenAI()

def ask_openai(mensagem):
    
    if(mensagem == ""):
        resposta = "Como posso ajudá-lo?"
        return resposta
    
    else: 
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            
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
                                        1. Reescrever de maneria diferente e técnica o caso de teste enviado dando 3 opções e enumerando eles no no campo <caso>
                                        2. Estipular o cenário de teste, de maneira resumida, e inseri-lo em <cenario> 
                                        3. Estipular os riscos atraledos em <riscos>
                                        4. Escrever pre-condições para realizar o teste em <precondicoes>
                                        5. Os passos no padrão gherkin para o caso de teste submetido, inserido em <gherkin>

                                        Utilize o seguinte exemplo para exibir a resposta como se fosse um arquivo json: 
                                        {
                                         "caso": "<caso>",
                                         "cenario":"<cenario>",
                                         "riscos": "<riscos>",
                                         "gherkin":"<gherkin>",
                                         "precondicoes":"<precondicoes>"
                                        }
                                       '''
                    }
                ],
                temperature=1,
                max_tokens=500,
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
    mensagem = st.text_input("Digite aqui o caso de teste:", label_visibility="hidden")
    st.write('''
             <p class="letra">Digite aqui o caso de teste</p>
             ''',unsafe_allow_html=True)
    
    if (mensagem == ""):
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

        with st.container():
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
                    <div>
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
                    ''', unsafe_allow_html=True)
            