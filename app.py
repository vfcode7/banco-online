import streamlit as st
from datetime import datetime
import pandas as pd

# Configuração da página
st.set_page_config(
    page_title="Banco Online",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Inicializar session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.usuario = ""
    st.session_state.saldo = 5000.00
    st.session_state.transacoes = [
        {"Data": "2024-01-10", "Tipo": "Transferência", "Valor": "-R$ 500,00", "Saldo": "R$ 4.500,00"},
        {"Data": "2024-01-09", "Tipo": "Depósito", "Valor": "+R$ 1.000,00", "Saldo": "R$ 5.000,00"},
        {"Data": "2024-01-08", "Tipo": "Saque", "Valor": "-R$ 200,00", "Saldo": "R$ 5.200,00"}
    ]

# ====== TELA DE LOGIN ======
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.title("🏦 Banco Online")
        st.write("---")
        
        with st.form("login_form"):
            st.subheader("Fazer Login")
            usuario = st.text_input("👤 Usuário", placeholder="Digite seu usuário")
            senha = st.text_input("🔐 Senha", type="password", placeholder="Digite sua senha")
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                submit = st.form_submit_button("Entrar", use_container_width=True)
            with col_btn2:
                registrar = st.form_submit_button("Registrar", use_container_width=True)
            
            if submit:
                # Validação simples (em produção, usar banco de dados)
                if usuario == "joao" and senha == "123456":
                    st.session_state.logged_in = True
                    st.session_state.usuario = usuario
                    st.success("✅ Login realizado com sucesso!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("❌ Usuário ou senha incorretos!")
                    st.info("📝 Teste: **joao** / **123456**")
            
            if registrar:
                st.info("📋 Funcionalidade de registro em desenvolvimento")

# ====== DASHBOARD PRINCIPAL ======
else:
    # Sidebar
    with st.sidebar:
        st.write(f"### 👤 {st.session_state.usuario}")
        st.write("---")
        
        if st.button("🚪 Sair", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.usuario = ""
            st.rerun()
    
    # Header
    st.title(f"🏦 Bem-vindo, {st.session_state.usuario}!")
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💰 Saldo", f"R$ {st.session_state.saldo:.2f}", "+R$ 200,00")
    
    with col2:
        st.metric("📊 Transações", "12", "+2")
    
    with col3:
        st.metric("💳 Limite", "R$ 2.000,00", "0")
    
    with col4:
        st.metric("📅 Última Atualização", datetime.now().strftime("%H:%M:%S"), "")
    
    st.write("---")
    
    # Menu de operações
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Extrato", "💸 Transferência", "💳 Pagamentos", "🔧 Configurações", "ℹ️ Informações"])
    
    # ABA 1: EXTRATO
    with tab1:
        st.subheader("📊 Extrato da Conta")
        
        # Filtros
        col1, col2 = st.columns(2)
        with col1:
            data_inicio = st.date_input("Data Inicial")
        with col2:
            data_fim = st.date_input("Data Final")
        
        # Tabela de transações
        df_transacoes = pd.DataFrame(st.session_state.transacoes)
        st.dataframe(df_transacoes, use_container_width=True)
        
        # Download
        csv = df_transacoes.to_csv(index=False)
        st.download_button(
            label="📥 Baixar Extrato (CSV)",
            data=csv,
            file_name="extrato.csv",
            mime="text/csv"
        )
    
    # ABA 2: TRANSFERÊNCIA
    with tab2:
        st.subheader("💸 Transferência Bancária")
        
        with st.form("transfer_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                banco = st.selectbox("Banco", ["Banco do Brasil", "Itaú", "Bradesco", "Caixa", "Outro"])
                agencia = st.text_input("Agência", placeholder="0000")
            
            with col2:
                tipo_conta = st.selectbox("Tipo de Conta", ["Corrente", "Poupança"])
                conta = st.text_input("Conta", placeholder="00000-0")
            
            nome_beneficiario = st.text_input("Nome do Beneficiário", placeholder="Digite o nome completo")
            cpf = st.text_input("CPF do Beneficiário", placeholder="000.000.000-00")
            valor = st.number_input("Valor (R$)", min_value=0.01, step=0.01, value=0.0)
            
            col1, col2 = st.columns(2)
            with col1:
                submit = st.form_submit_button("✅ Confirmar Transferência", use_container_width=True)
            with col2:
                limpar = st.form_submit_button("🔄 Limpar", use_container_width=True)
            
            if submit:
                if valor <= 0:
                    st.error("❌ Digite um valor válido!")
                elif valor > st.session_state.saldo:
                    st.error("❌ Saldo insuficiente!")
                else:
                    st.success(f"✅ Transferência de R$ {valor:.2f} enviada para {nome_beneficiario}!")
                    st.session_state.saldo -= valor
                    st.session_state.transacoes.insert(0, {
                        "Data": datetime.now().strftime("%Y-%m-%d"),
                        "Tipo": "Transferência",
                        "Valor": f"-R$ {valor:.2f}",
                        "Saldo": f"R$ {st.session_state.saldo:.2f}"
                    })
    
    # ABA 3: PAGAMENTOS
    with tab3:
        st.subheader("💳 Pagamentos de Contas")
        
        with st.form("payment_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                tipo = st.selectbox("Tipo de Pagamento", ["Energia Elétrica", "Água", "Internet", "Telefone", "Boleto"])
            
            with col2:
                valor = st.number_input("Valor (R$)", min_value=0.01, step=0.01, value=0.0)
            
            codigo = st.text_input("Código de Barras / Referência", placeholder="Digite o código")
            
            col1, col2 = st.columns(2)
            with col1:
                submit = st.form_submit_button("✅ Realizar Pagamento", use_container_width=True)
            with col2:
                limpar = st.form_submit_button("🔄 Limpar", use_container_width=True)
            
            if submit:
                if valor <= 0:
                    st.error("❌ Digite um valor válido!")
                elif valor > st.session_state.saldo:
                    st.error("❌ Saldo insuficiente!")
                else:
                    st.success(f"✅ Pagamento de R$ {valor:.2f} ({tipo}) realizado com sucesso!")
                    st.session_state.saldo -= valor
                    st.session_state.transacoes.insert(0, {
                        "Data": datetime.now().strftime("%Y-%m-%d"),
                        "Tipo": f"Pagamento - {tipo}",
                        "Valor": f"-R$ {valor:.2f}",
                        "Saldo": f"R$ {st.session_state.saldo:.2f}"
                    })
    
    # ABA 4: CONFIGURAÇÕES
    with tab4:
        st.subheader("⚙️ Configurações da Conta")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("### 🔐 Alterar Senha")
            with st.form("password_form"):
                senha_atual = st.text_input("Senha Atual", type="password")
                senha_nova = st.text_input("Nova Senha", type="password")
                confirmar = st.text_input("Confirmar Senha", type="password")
                
                if st.form_submit_button("Atualizar Senha", use_container_width=True):
                    if len(senha_nova) < 6:
                        st.error("❌ Senha deve ter pelo menos 6 caracteres!")
                    elif senha_nova != confirmar:
                        st.error("❌ As senhas não coincidem!")
                    else:
                        st.success("✅ Senha atualizada com sucesso!")
        
        with col2:
            st.write("### 📱 Dados Cadastrais")
            st.info(f"**Usuário**: {st.session_state.usuario}\n\n**CPF**: 123.456.789-00\n\n**Email**: {st.session_state.usuario}@email.com")
    
    # ABA 5: INFORMAÇÕES
    with tab5:
        st.subheader("ℹ️ Informações da Conta")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("### 🏦 Dados Bancários")
            st.write("""
            - **Banco**: Banco Online Demo
            - **Agência**: 0001
            - **Conta**: 123456-7
            - **Tipo**: Corrente
            """)
        
        with col2:
            st.write("### 📊 Resumo")
            st.write(f"""
            - **Saldo Disponível**: R$ {st.session_state.saldo:.2f}
            - **Limite**: R$ 2.000,00
            - **Saldo Total**: R$ {st.session_state.saldo + 2000:.2f}
            - **Última Atualização**: {datetime.now().strftime("%d/%m/%Y %H:%M")}
            """)

