import streamlit as st

st.set_page_config(page_title="Banco Online", layout="centered")

st.title("🏦 Banco Online")

# Login
usuario = st.text_input("Usuário")
senha = st.text_input("Senha", type="password")

if st.button("Entrar"):
    if usuario == "joao" and senha == "123456":
        st.success("Login bem-sucedido!")
        st.balloons()
    else:
        st.error("Usuário ou senha incorretos")
