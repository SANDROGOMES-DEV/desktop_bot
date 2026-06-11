import streamlit as st
import time
from core.engine import CommandEngine

# ==========================================
# Configuração de View (Front-end)
# ==========================================
st.set_page_config(page_title="Automator Engine", page_icon="⚙️")

# Singleton da Engine no Session State para não recriar a cada re-render do Streamlit
if 'engine' not in st.session_state:
    st.session_state.engine = CommandEngine()

st.title("⚙️ Automator Engine v2.0")
st.markdown("Arquitetura Modular Baseada em Princípios S.O.L.I.D.")
st.markdown("---")

# ==========================================
# Componentes de UI
# ==========================================
comando = st.text_input("Terminal de Comando", placeholder="Ex: acesse site github.com")

if st.button("Executar Ação", type="primary", use_container_width=True):
    if comando:
        # Feedback visual antes do processamento (especial para PyAutoGUI)
        if "digite" in comando.lower():
            st.warning("⏳ O bot assumirá o teclado em 3 segundos. Clique na janela desejada AGORA!")
            # Um pequeno truque de UI para renderizar o warning antes do bloqueio de thread
            time.sleep(0.1)

        with st.spinner("Processando instrução na Engine..."):
            # Delega a lógica de negócios para a camada 'core'
            resultado = st.session_state.engine.process(comando)

            # Tratamento da resposta
            if resultado["status"] == "success":
                st.success(resultado["message"])
            else:
                st.error(resultado["message"])
    else:
        st.warning("Por favor, forneça uma instrução válida.")

# ==========================================
# Footer
# ==========================================
st.markdown("---")
st.caption("Sistema desacoplado. Pronto para integração com APIs de LLM (OpenAI/Anthropic).")
