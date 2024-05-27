import streamlit as st
import pandas as pd

st.set_page_config(
  layout="wide"
)

if 'df' not in st.session_state:
  try:
    st.session_state['df'] = pd.read_csv('dados.csv')
  except FileNotFoundError:
    st.session_state['df'] = pd.DataFrame(columns=["Produto","Fornecedor", "Quantidade","Lote","Estado físico","Validade"])

col1, col2 = st.columns(2)
col3, col4 = st.columns(2)
# Título da aplicação
with col1:
  st.title("Coletar e Armazenar Dados")
  # Formulário para coletar dados
  with st.form(key='data_form'):
    produto = st.text_input("Produto químico")
    fornecedor = st.text_input("Fornecedor")
    quantidade = st.number_input("Quantidade")
    lote = st.text_input("Lote:")
    estado_fisico = st.selectbox("Estado Físico:", ["Sólido", "Líquido", "Gasoso"])
    validade = st.date_input("Validade:")
    submit_button = st.form_submit_button(label='Enviar')

  # Criação do dataframe vazio ou carregado de um arquivo existente
    if submit_button:
      if not produto or not fornecedor or not estado_fisico or quantidade == 0: 
        st.error('Insira os valores nos campos obrigatórios')
      else: 
        new_data = pd.DataFrame({
                                  "Produto": [produto], 
                                  "Fornecedor": [fornecedor], 
                                  "Quantidade":[quantidade],
                                  "Lote":[lote], 
                                  "Estado físico":[estado_fisico],
                                  "Validade":[validade]
                                  })
        st.session_state['df'] = pd.concat([st.session_state['df'], new_data], ignore_index=True)
        st.session_state['df'].to_csv('dados.csv', index=False)
        st.success("Dados adicionados com sucesso!")
        


with col2: 
  st.header("Tabela de arquivos salvos")   
  st.write(st.session_state['df'])

  # Apagando dataframe
  st.subheader("Remover Dados")
  index_to_remove = st.number_input("Índice da linha a remover:", min_value=0, max_value=len(st.session_state['df'])-1, step=1)
  if st.button('Remover'):
      if 0 <= index_to_remove < len(st.session_state['df']):
        st.session_state['df'] = st.session_state['df'].drop(index_to_remove).reset_index(drop=True)
        st.session_state['df'].to_csv('dados.csv', index=False)
        st.success("Linha removida com sucesso!")
        st.experimental_rerun()
      else:
        st.error("Erro: Índice inválido")
  #Alterando os campos através do índice
  st.header("Editar dados")   
  index_to_edit = st.number_input("Índice da linha a editar:", min_value=0, max_value=len(st.session_state['df'])-1, step=1)   
  if st.button('Carregar Dados para Edição'):
        if 0 <= index_to_edit < len(st.session_state['df']):
          editable_data = st.session_state['df'].iloc[index_to_edit]
          produto_edit = st.text_input("Produto", value=editable_data["Produto"])
          fornecedor_edit = st.text_input("Fornecedor", value=editable_data["Fornecedor"])
          lote_edit = st.text_input("Lote", value=editable_data["Lote"])
          quantidade_edit = st.number_input("Quantidade:", value=editable_data["Quantidade"])
          estado_fisico_edit = st.selectbox("Estado Físico:", ["Sólido", "Líquido", "Gasoso"], index=["Sólido", "Líquido", "Gasoso"].index(editable_data["Estado físico"]))
          data_edit = st.date_input("Validade:", value=pd.to_datetime(editable_data["Validade"]))

          if st.button('Salvar Alterações'):
            st.session_state['df'].at[index_to_edit, 'Produto'] = produto_edit
            st.session_state['df'].at[index_to_edit, 'Fornecedor'] = fornecedor_edit
            st.session_state['df'].at[index_to_edit, 'Quantidade'] = quantidade_edit
            st.session_state['df'].at[index_to_edit, 'Estado físico'] = estado_fisico_edit
            st.session_state['df'].at[index_to_edit, 'Lote'] = lote_edit
            st.session_state['df'].at[index_to_edit, 'Data'] = data_edit
            st.session_state['df'].to_csv('dados.csv', index=False)
            st.success("Dados atualizados com sucesso!")
            st.experimental_rerun()  # Recarregar a página para refletir as mudanças
        else:
            st.error("Erro: Índice Inexistente")