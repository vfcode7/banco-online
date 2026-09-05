import streamlit as st

st.set_page_config(page_title="Banco Online", layout="centered")
st.title("🏦 Banco Online")

# Login simples
usuario = st.text_input("Usuário")
senha = st.text_input("Senha", type="password")

if st.button("Entrar"):
    if usuario == "joao" and senha == "123456":
        st.success("Login bem-sucedido! 👋")
        st.balloons()
        
        # Dashboard após login
        st.divider()
        st.subheader("📊 Dashboard")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Saldo", "R$ 5.000,00", "+R$ 200,00")
        with col2:
            st.metric("Transações", "12", "+2")
        with col3:
            st.metric("Limite", "R$ 2.000,00", "0")
        
        st.divider()
        
        # Menu de operações
        opcao = st.selectbox(
            "Selecione uma operação:",
            ["Extrato", "Transferência", "Pagamentos", "Configurações"]
        )
        
        if opcao == "Extrato":
            st.subheader("📊 Extrato da Conta")
            st.write("Últimas transações:")
            
            data = {
                "Data": ["2024-01-10", "2024-01-09", "2024-01-08"],
                "Tipo": ["Transferência", "Depósito", "Saque"],
                "Valor": ["-R$ 500,00", "+R$ 1.000,00", "-R$ 200,00"],
                "Saldo": ["R$ 4.500,00", "R$ 5.000,00", "R$ 5.200,00"]
            }
            st.dataframe(data)
        
        elif opcao == "Transferência":
            st.subheader("💸 Transferência")
            with st.form("transfer_form"):
                dest_account = st.text_input("Conta de destino")
                amount = st.number_input("Valor (R$)", min_value=0.0, step=0.01)
                submitted = st.form_submit_button("Enviar")
                
                if submitted and amount > 0:
                    st.success(f"Transferência de R$ {amount:.2f} enviada para {dest_account}!")
        
        elif opcao == "Pagamentos":
            st.subheader("💳 Pagamentos")
            with st.form("payment_form"):
                biller = st.selectbox("Beneficiário", ["Luz", "Água", "Internet", "Outro"])
                amount = st.number_input("Valor (R$)", min_value=0.0, step=0.01)
                submitted = st.form_submit_button("Pagar")
                
                if submitted and amount > 0:
                    st.success(f"Pagamento de R$ {amount:.2f} realizado!")
        
        elif opcao == "Configurações":
            st.subheader("⚙️ Configurações")
            new_password = st.text_input("Nova senha", type="password")
            confirm_password = st.text_input("Confirmar senha", type="password")
            
            if st.button("Atualizar Senha"):
                if new_password == confirm_password and len(new_password) >= 6:
                    st.success("Senha atualizada com sucesso!")
                else:
                    st.error("As senhas não coincidem ou são muito curtas!")
    else:
        st.error("Usuário ou senha incorretos!")
        st.info("Tente com: **joao** / **123456**")
