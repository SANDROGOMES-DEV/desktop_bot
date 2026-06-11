import sys
import asyncio
import streamlit as st
import time
from dotenv import load_dotenv
from core.engine import CommandEngine

# 1. Carrega as variáveis secretas do ficheiro .env para a memória
load_dotenv()

# Corrige o WinError 10054 do ProactorEventLoop no Windows
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Configuração da página Streamlit
st.set_page_config(page_title="Automator Engine AI", page_icon="⚙️", layout="wide")

# Inicializa a Engine e liga a IA no estado da sessão
if 'engine' not in st.session_state:
    st.session_state.engine = CommandEngine()

    # Tenta ligar a IA automaticamente (o None obriga a procurar no .env)
    try:
        st.session_state.engine.enable_ai(None)
        st.session_state.ai_status = "✅ Cérebro de IA Conectado com Sucesso (Segurança Ativa)"
    except ValueError:
        st.session_state.ai_status = "⚠️ Modo Básico: IA Desligada (Ficheiro .env não configurado)"

# ==========================================
# View Principal (Interface do Utilizador)
# ==========================================
st.title("⚙️ Automator Engine v3.0 (Powered by AI)")
st.caption(st.session_state.ai_status)
st.markdown("---")

# Campo de entrada
comando = st.text_input(
    "Terminal de Comando",
    placeholder="Ex: 'Mano, podes fazer o favor de pesquisar sobre Python no google?'"
)

# Botão de Execução
if st.button("Executar Ação", type="primary", use_container_width=True):
    if comando:
        # Se for um comando de digitação direto (sem IA), avisa sobre os 3 segundos
        if "digite" in comando.lower() and "⚠️" in st.session_state.ai_status:
            st.warning("⏳ O bot assumirá o teclado em 3 segundos. Clica na janela desejada AGORA!")
            time.sleep(0.1)

        with st.spinner("O Cérebro está a processar a tua instrução..."):
            # Envia para a Engine (que vai passar pela IA se estiver ligada)
            resultado = st.session_state.engine.process(comando)

            # Mostra o resultado final
            if resultado["status"] == "success":
                st.success(resultado["message"])
            else:
                st.error(resultado["message"])
    else:
        st.warning("Por favor, fornece uma instrução válida antes de executar.")
