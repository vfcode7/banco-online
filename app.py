import streamlit as st
from datetime import datetime
import pandas as pd
import json
import os

# ====== CONFIGURAÇÃO ======
st.set_page_config(
    page_title="Banco Online",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# ====== FUNÇÕES DE PERSISTÊNCIA ======
DATA_FILE = "banco_dados.json"

def carregar_dados():
    """Carrega dados do arquivo JSON"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {
        "usuarios": {
            "joao": {"senha": "123456", "saldo": 5000.00, "transacoes": []},
            "maria": {"senha": "senha456", "saldo": 10000.00, "transacoes": []}
        }
    }

def salvar_dados(dados):
    """Salva dados no arquivo JSON"""
    with open(DATA_FILE, "w") as f:
        json.dump(dados, f, indent=4)

def adicionar_transacao(usuario, tipo, valor, descricao=""):
    """Adiciona transação e atualiza saldo"""
    dados = carregar_dados()
    if usuario in dados["usuarios"]:
        dados["usuarios"][usuario]["transacoes"].insert(0, {
            "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "tipo": tipo,
            "valor": f"-R$ {valor:.2f}" if "Transferência" in tipo or "Pagamento" in tipo or "Saque" in tipo else f"+R$ {valor:.2f}",
            "descricao": descricao,
            "saldo": f"R$ {dados['usuarios'][usuario]['saldo']:.2f}"
        })
        salvar_dados(dados)

# ====== INICIALIZAR SESSION STATE ======
dados_globais = carregar_dados()

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.usuario = ""

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
                dados = carregar_dados()
                if usuario in dados["usuarios"] and dados["usuarios"][usuario]["senha"] == senha:
                    st.session_state.logged_in = True
                    st.session_state.usuario = usuario
                    st.success("✅ Login realizado com sucesso!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("❌ Usuário ou senha incorretos!")
                    st.info("📝 Teste: **joao/123456** ou **maria/senha456**")
            
            if registrar:
                st.info("📋 Funcionalidade de registro em desenvolvimento")

# ====== DASHBOARD PRINCIPAL ======
else:
    dados = carregar_dados()
    usuario_data = dados["usuarios"][st.session_state.usuario]
    saldo = usuario_data["saldo"]
    transacoes = usuario_data["transacoes"]
    
    # Sidebar
    with st.sidebar:
        st.write(f"### 👤 {st.session_state.usuario}")
        st.write(f"**Saldo**: R$ {saldo:.2f}")
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
        st.metric("💰 Saldo", f"R$ {saldo:.2f}")
    
    with col2:
        st.metric("📊 Transações", len(transacoes))
    
    with col3:
        st.metric("💳 Limite", "R$ 2.000,00")
    
    with col4:
        st.metric("📅 Hora", datetime.now().strftime("%H:%M:%S"))
    
    st.write("---")
    
    # Menu de operações
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Extrato", "💸 Transferência", "💳 Pagamentos", "🔧 Configurações", "ℹ️ Informações"])
    
    # ABA 1: EXTRATO
    with tab1:
        st.subheader("📊 Extrato da Conta")
        
        if transacoes:
            df_transacoes = pd.DataFrame(transacoes)
            st.dataframe(df_transacoes, use_container_width=True)
            
            # Download
            csv = df_transacoes.to_csv(index=False)
            st.download_button(
                label="📥 Baixar Extrato (CSV)",
                data=csv,
                file_name="extrato.csv",
                mime="text/csv"
            )
        else:
            st.info("📭 Nenhuma transação registrada")
    
    # ABA 2: TRANSFERÊNCIA
    with tab2:
        st.subheader("💸 Transferência Bancária")
        
        with st.form("transfer_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                banco = st.selectbox("Banco", ["Banco do Brasil", "Itaú", "Bradesco", "Caixa", "Outro"], key="banco_trans")
                agencia = st.text_input("Agência", placeholder="0000", key="agencia_trans")
            
            with col2:
                tipo_conta = st.selectbox("Tipo de Conta", ["Corrente", "Poupança"], key="tipo_conta_trans")
                conta = st.text_input("Conta", placeholder="00000-0", key="conta_trans")
            
            nome_beneficiario = st.text_input("Nome do Beneficiário", placeholder="Digite o nome completo", key="nome_bene")
            cpf = st.text_input("CPF do Beneficiário", placeholder="000.000.000-00", key="cpf_trans")
            valor = st.number_input("Valor (R$)", min_value=0.01, step=0.01, value=0.0, key="valor_trans")
            
            col1, col2 = st.columns(2)
            with col1:
                submit = st.form_submit_button("✅ Confirmar Transferência", use_container_width=True)
            with col2:
                st.form_submit_button("🔄 Limpar", use_container_width=True)
            
            if submit:
                if valor <= 0:
                    st.error("❌ Digite um valor válido!")
                elif valor > saldo:
                    st.error("❌ Saldo insuficiente!")
                else:
                    # Atualizar dados
                    dados = carregar_dados()
                    dados["usuarios"][st.session_state.usuario]["saldo"] -= valor
                    adicionar_transacao(st.session_state.usuario, "Transferência", valor, f"para {nome_beneficiario}")
                    salvar_dados(dados)
                    
                    st.success(f"✅ Transferência de R$ {valor:.2f} enviada para {nome_beneficiario}!")
                    st.rerun()
    
    # ABA 3: PAGAMENTOS
    with tab3:
        st.subheader("💳 Pagamentos de Contas")
        
        with st.form("payment_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                tipo = st.selectbox("Tipo de Pagamento", ["Energia Elétrica", "Água", "Internet", "Telefone", "Boleto"], key="tipo_pag")
            
            with col2:
                valor = st.number_input("Valor (R$)", min_value=0.01, step=0.01, value=0.0, key="valor_pag")
            
            codigo = st.text_input("Código de Barras / Referência", placeholder="Digite o código", key="codigo_pag")
            
            col1, col2 = st.columns(2)
            with col1:
                submit = st.form_submit_button("✅ Realizar Pagamento", use_container_width=True)
            with col2:
                st.form_submit_button("🔄 Limpar", use_container_width=True)
            
            if submit:
                if valor <= 0:
                    st.error("❌ Digite um valor válido!")
                elif valor > saldo:
                    st.error("❌ Saldo insuficiente!")
                else:
                    # Atualizar dados
                    dados = carregar_dados()
                    dados["usuarios"][st.session_state.usuario]["saldo"] -= valor
                    adicionar_transacao(st.session_state.usuario, f"Pagamento - {tipo}", valor, codigo)
                    salvar_dados(dados)
                    
                    st.success(f"✅ Pagamento de R$ {valor:.2f} ({tipo}) realizado com sucesso!")
                    st.rerun()
    
    # ABA 4: CONFIGURAÇÕES
    with tab4:
        st.subheader("⚙️ Configurações da Conta")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("### 🔐 Alterar Senha")
            with st.form("password_form"):
                senha_atual = st.text_input("Senha Atual", type="password", key="senha_atual")
                senha_nova = st.text_input("Nova Senha", type="password", key="senha_nova")
                confirmar = st.text_input("Confirmar Senha", type="password", key="confirmar_senha")
                
                if st.form_submit_button("Atualizar Senha", use_container_width=True):
                    dados = carregar_dados()
                    if dados["usuarios"][st.session_state.usuario]["senha"] != senha_atual:
                        st.error("❌ Senha atual incorreta!")
                    elif len(senha_nova) < 6:
                        st.error("❌ Senha deve ter pelo menos 6 caracteres!")
                    elif senha_nova != confirmar:
                        st.error("❌ As senhas não coincidem!")
                    else:
                        dados["usuarios"][st.session_state.usuario]["senha"] = senha_nova
                        salvar_dados(dados)
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
            - **Saldo Disponível**: R$ {saldo:.2f}
            - **Limite**: R$ 2.000,00
            - **Saldo Total**: R$ {saldo + 2000:.2f}
            - **Última Atualização**: {datetime.now().strftime("%d/%m/%Y %H:%M")}
            """)
