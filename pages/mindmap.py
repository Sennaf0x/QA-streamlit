import streamlit as st
from openai import OpenAI
import json
import streamlit.components.v1 as components
import pandas as pd


if "resposta" not in st.session_state:
    st.session_state.resposta = '''
# Tópico Principal
## Subtópico 1
 - Ponto 1
  - Detalhe 1
  - Detalhe 2
 - Ponto 2
## Subtópico 2
 - Ponto 1
 - Ponto 2
  - Detalhe 1
    - Subdetalhe 1
    - Subdetalhe 2
## Subtópico 3
 - Ponto 1
 - Ponto 2
 - Ponto 3
## Conclusão
 - Resumo dos tópicos
 - Considerações finais
        '''

client = OpenAI()

df = ''

def ask_openai(df):
    if df == '':
        return "Como posso ajudá-lo?"
    try:
        print("Iniciando chat")
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
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
                                    Leia os casos de teste da planilha {df} e crie uma resposta em markdown:
                                    \n
                                    Exemplo de markdwn
                                    # Lista de processo de vítima
                                    ## Cenário Positivo (Caminho Feliz)
                                    ### O usuário acessa a tela de 'Adicionar processo' sem dados cadastrados. 
                                    #### Casos de Teste
                                     - Validar se ao acessar a tela de 'Adicionar processo', os campos descritos estarão limpos: 
                                     - Campos válidos: 'Arquivos anexados', 'Processo', 'Data de término do processo', 'Descrição', 'Associar agressor ao processo'. 
                                     - Validar se ao acessar a tela de 'Adicionar processo', alguns campos serão carregados com valores iniciais:
                                       - Exceção: 'Raio: 100', 'Margem de tolerâncias: 10'. 
                                     - Validar se a opção 'Salvar' iniciará desabilitada e a opção 'Voltar' habilitada. 
                                    ### O usuário cadastra um novo processo na tela de 'Cadastrar vítima - processo'. 
                                    #### Casos de Teste 
                                     - Validar se os campos 'Arquivos anexados', 'Processo', 'Data de término do processo', 'Descrição', 'Associar agressor ao processo' e 'Raio' são obrigatórios. 
                                     - Validar se ao associar um agressor, um card com informações será exibido no sistema: 
                                       - Informações: 'Nome', 'Data de nascimento', 'Nome social', 'Status', 'Nome da mãe'. 
                                     - Validar se na tela de 'Adicionar processo', o campo 'Associar agressor ao processo', após digitação de qualquer dado sobre o agressor, o sistema irá exibir uma lista com os resultados válidos. 
                                    ## Caminho Alternativo 
                                    ### O usuário não conclui o cadastro de uma vítima. 
                                    #### Casos de Teste 
                                     - Validar se, ao selecionar a opção 'Voltar', o usuário será redirecionado para a tela de 'Cadastrar vítima - processo' e terá os dados descartados. 
                                     - Validar se, caso o usuário não preencha todos os campos da maneira correta e selecione a opção 'Salvar', um alerta será gerado no respectivo campo. 
                                     - Validar se, caso o número do processo esteja duplicado, será exibida uma mensagem de alerta: 
                                       - Mensagem: 'Número do processo já existe para outra vítima.'

                                ''')
                }
            ],

            temperature=1,
            max_tokens=10000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0

            )
        
        answer = completion.choices[0].message.content
        answer = answer.replace('`','').replace('json','')
        print(f"answer: {answer}")
        return answer
    
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON: {e}")
        return None

    except Exception as e:
        print(f"Erro inesperado: {e}")
        return None

with st.form("upload"):
    nome = st.text_input("Nome do arquivo")
    dados = st.file_uploader("Insira a planilha em excel", type=["xlsx"])
    enviar = st.form_submit_button("Markdown")
    
    if enviar:
        df = pd.read_excel(dados)
        st.dataframe(df)
        
        json_df = df.to_json(orient='records',force_ascii=True,lines=True)
        resposta = ask_openai(json_df)
        st.session_state.resposta = resposta
        print(f"Resposta do chat: {st.session_state.resposta}")
        


with st.container():
                    
    html_markdown ='''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta http-equiv="X-UA-Compatible" content="IE=edge" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Markmap</title>
        <style>
        svg.markmap {
            width: 100%;
            height: 100vh;
        }
        .markmap-foreign {
            width: 350px;
        }
        div {
            padding: 10px;
            }    
        </style>
        <script src="https://cdn.jsdelivr.net/npm/markmap-autoloader@0.16"></script>
        <script src="https://html2canvas.hertzen.com/dist/html2canvas.min.js"></script>
    </head>
    <body>
        <button id="exportButton">Export as PNG</button>
        <div id="mindmap-container" class="markmap">
        <script type="text/template">
            ---
            markmap:
              maxWidth: 400
              colorFreezeLevel: 5
              spacingVertical: 100
            ---
            ''' + f'''
            {st.session_state.resposta}
            ''' + '''

        </script>
        </div>
        <script>
            document.getElementById('exportButton').addEventListener('click', function() {
            html2canvas(document.querySelector("#mindmap-container"), {scale: 5}).then(canvas => {
            var link = document.createElement('a');''' + f'''
            link.download = '{nome}.png';''' + '''
            link.href = canvas.toDataURL();
            link.click();
              });
            });
        </script>
    </body>
    </html>
    '''
    
    imagem = st.components.v1.html(html_markdown, height=600)