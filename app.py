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
    .main { padding: 2rem; }
    body { background-color: #f0f2f6; }
</style>
""", unsafe_allow_html=True)

# ====== ARQUIVO DE DADOS ======
DATA_FILE = "banco_dados.json"

@st.cache_data
def criar_dados_padrao():
    """Cria dados padrão se não existir"""
    return {
        "usuarios": {
            "joao": {"senha": "123456", "saldo": 5000.00, "transacoes": []},
            "maria": {"senha": "senha456", "saldo": 10000.00, "transacoes": []}
        }
    }

def carregar_dados():
    """Carrega dados do arquivo"""
    if not os.path.exists(DATA_FILE):
        dados = criar_dados_padrao()
        with open(DATA_FILE, "w") as f:
            json.dump(dados, f, indent=4)
        return dados
    
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def salvar_dados(dados):
    """Salva dados no arquivo"""
    with open(DATA_FILE, "w") as f:
        json.dump(dados, f, indent=4)
    st.cache_data.clear()

# ====== INICIALIZAR SESSION STATE ======
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.usuario = ""

if 'tab_ativa' not in st.session_state:
    st.session_state.tab_ativa = 0

# ====== TELA DE LOGIN ======
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.title("🏦 Banco Online")
        st.write("---")
        
        st.subheader("Fazer Login")
        usuario = st.text_input("👤 Usuário", placeholder="Digite seu usuário", key="login_user")
        senha = st.text_input("🔐 Senha", type="password", placeholder="Digite sua senha", key="login_pass")
        
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            if st.button("✅ Entrar", use_container_width=True, key="btn_login"):
                dados = carregar_dados()
                if usuario and usuario in dados["usuarios"] and dados["usuarios"][usuario]["senha"] == senha:
                    st.session_state.logged_in = True
                    st.session_state.usuario = usuario
                    st.success("✅ Login realizado com sucesso!")
                    st.balloons()
                    st.rerun()
                elif usuario:
                    st.error("❌ Usuário ou senha incorretos!")
                else:
                    st.error("❌ Digite um usuário!")
        
        with col_btn2:
            if st.button("📋 Registrar", use_container_width=True, key="btn_registrar"):
                st.info("Funcionalidade em desenvolvimento")
        
        st.info("📝 Teste: **joao/123456** ou **maria/senha456**")

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
        
        if st.button("🚪 Sair", use_container_width=True, key="btn_sair"):
            st.session_state.logged_in = False
            st.session_state.usuario = ""
            st.rerun()
    
    # Header
    st.title(f"🏦 Bem-vindo, {st.session_state.usuario}!")
    
    # Métricas
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💰 Saldo", f"R$ {saldo:.2f}")
    with col2:
        st.metric("📊 Transações", len(transacoes))
    with col3:
        st.metric("💳 Limite", "R$ 2.000,00")
    with col4:
        st.metric("⏰ Hora", datetime.now().strftime("%H:%M:%S"))
    
    st.write("---")
    
    # Menu
    opcao = st.selectbox(
        "📋 Selecione uma opção:",
        ["📊 Extrato", "💸 Transferência", "💳 Pagamentos", "🔧 Configurações", "ℹ️ Informações"],
        key="menu_principal"
    )
    
    st.write("---")
    
    # ====== EXTRATO ======
    if opcao == "📊 Extrato":
        st.subheader("📊 Extrato da Conta")
        
        if transacoes:
            df = pd.DataFrame(transacoes)
            st.dataframe(df, use_container_width=True)
            
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Baixar Extrato (CSV)",
                data=csv,
                file_name="extrato.csv",
                mime="text/csv",
                key="download_extrato"
            )
        else:
            st.info("📭 Nenhuma transação registrada")
    
    # ====== TRANSFERÊNCIA ======
    elif opcao == "💸 Transferência":
        st.subheader("💸 Transferência Bancária")
        
        banco = st.selectbox("🏦 Banco", ["Banco do Brasil", "Itaú", "Bradesco", "Caixa", "Outro"], key="sel_banco")
        agencia = st.text_input("Agência", placeholder="0000", key="inp_agencia")
        tipo_conta = st.selectbox("Tipo de Conta", ["Corrente", "Poupança"], key="sel_tipo_conta")
        conta = st.text_input("Conta", placeholder="00000-0", key="inp_conta")
        nome_beneficiario = st.text_input("Nome do Beneficiário", placeholder="Digite o nome completo", key="inp_nome")
        cpf = st.text_input("CPF do Beneficiário", placeholder="000.000.000-00", key="inp_cpf")
        valor = st.number_input("Valor (R$)", min_value=0.01, step=0.01, value=100.0, key="inp_valor_trans")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("✅ Confirmar Transferência", use_container_width=True, key="btn_trans"):
                if not nome_beneficiario:
                    st.error("❌ Digite o nome do beneficiário!")
                elif valor > saldo:
                    st.error(f"❌ Saldo insuficiente! Saldo: R$ {saldo:.2f}")
                else:
                    # Atualizar dados
                    dados = carregar_dados()
                    dados["usuarios"][st.session_state.usuario]["saldo"] -= valor
                    
                    dados["usuarios"][st.session_state.usuario]["transacoes"].insert(0, {
                        "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "tipo": "Transferência",
                        "valor": f"-R$ {valor:.2f}",
                        "descricao": f"Para {nome_beneficiario}",
                        "saldo": f"R$ {dados['usuarios'][st.session_state.usuario]['saldo']:.2f}"
                    })
                    
                    salvar_dados(dados)
                    st.success(f"✅ Transferência de R$ {valor:.2f} enviada com sucesso!")
                    st.rerun()
        
        with col2:
            if st.button("🔄 Limpar Campos", use_container_width=True, key="btn_limpar_trans"):
                st.rerun()
    
    # ====== PAGAMENTOS ======
    elif opcao == "💳 Pagamentos":
        st.subheader("💳 Pagamentos de Contas")
        
        tipo = st.selectbox("Tipo de Pagamento", ["Energia Elétrica", "Água", "Internet", "Telefone", "Boleto"], key="sel_tipo_pag")
        valor = st.number_input("Valor (R$)", min_value=0.01, step=0.01, value=100.0, key="inp_valor_pag")
        codigo = st.text_input("Código de Barras / Referência", placeholder="Digite o código", key="inp_codigo_pag")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("✅ Realizar Pagamento", use_container_width=True, key="btn_pagar"):
                if valor > saldo:
                    st.error(f"❌ Saldo insuficiente! Saldo: R$ {saldo:.2f}")
                else:
                    # Atualizar dados
                    dados = carregar_dados()
                    dados["usuarios"][st.session_state.usuario]["saldo"] -= valor
                    
                    dados["usuarios"][st.session_state.usuario]["transacoes"].insert(0, {
                        "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "tipo": f"Pagamento - {tipo}",
                        "valor": f"-R$ {valor:.2f}",
                        "descricao": codigo,
                        "saldo": f"R$ {dados['usuarios'][st.session_state.usuario]['saldo']:.2f}"
                    })
                    
                    salvar_dados(dados)
                    st.success(f"✅ Pagamento de R$ {valor:.2f} realizado com sucesso!")
                    st.rerun()
        
        with col2:
            if st.button("🔄 Limpar Campos", use_container_width=True, key="btn_limpar_pag"):
                st.rerun()
    
    # ====== CONFIGURAÇÕES ======
    elif opcao == "🔧 Configurações":
        st.subheader("⚙️ Configurações da Conta")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("### 🔐 Alterar Senha")
            senha_atual = st.text_input("Senha Atual", type="password", key="inp_senha_atual")
            senha_nova = st.text_input("Nova Senha", type="password", key="inp_senha_nova")
            confirmar = st.text_input("Confirmar Senha", type="password", key="inp_confirmar_senha")
            
            if st.button("✅ Atualizar Senha", use_container_width=True, key="btn_alterar_senha"):
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
            st.info(f"""
            **Usuário**: {st.session_state.usuario}
            
            **CPF**: 123.456.789-00
            
            **Email**: {st.session_state.usuario}@email.com
            
            **Telefone**: (11) 99999-9999
            """)
    
    # ====== INFORMAÇÕES ======
    elif opcao == "ℹ️ Informações":
        st.subheader("ℹ️ Informações da Conta")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("### 🏦 Dados Bancários")
            st.write("""
            - **Banco**: Banco Online Demo
            - **Agência**: 0001
            - **Conta**: 123456-7
            - **Tipo**: Corrente
            - **Status**: Ativa
            """)
        
        with col2:
            st.write("### 📊 Resumo Financeiro")
            st.write(f"""
            - **Saldo Disponível**: R$ {saldo:.2f}
            - **Limite**: R$ 2.000,00
            - **Saldo Total**: R$ {saldo + 2000:.2f}
            - **Total Transações**: {len(transacoes)}
            - **Última Atualização**: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
            """)
