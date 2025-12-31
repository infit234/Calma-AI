import streamlit as st
import time

# 1. FORZAR DISEÑO DESDE EL INICIO
st.set_page_config(page_title="Calma", page_icon="🌿")

# Inyección de CSS ultra-específica
st.markdown("""
<style>
    /* Fondo Verde Menta Claro */
    .stApp { 
        background-color: #DFFFD6 !important; 
    }
    
    /* Texto Negro en TODO */
    * {
        color: #000000 !important;
    }

    /* Título Verde Oscuro */
    h1 { 
        color: #1B5E20 !important;
        text-align: center !important;
        font-weight: bold !important;
    }

    /* Forzar burbujas de chat blancas */
    div[data-testid="stChatMessage"] {
        background-color: #FFFFFF !important;
        border: 2px solid #A5D6A7 !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("Calma 🌿")
st.markdown("<h3 style='text-align: center;'>Your safe space. Speak freely.</h3>", unsafe_allow_html=True)

# 2. LÓGICA DE ESTADO (Para evitar la repetición)
if "messages" not in st.session_state:
    st.session_state.messages = []
if "done" not in st.session_state:
    st.session_state.done = False

# MOSTRAR HISTORIAL
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])

# 3. INPUT DE AUDIO
# Si ya terminó la simulación, no mostramos el input para evitar bucles
if not st.session_state.done:
    audio_value = st.audio_input("Record your voice")

    if audio_value:
        with st.spinner("Calma is listening... 🌿"):
            time.sleep(2) # Pausa dramática
            
            # Agregamos los mensajes al estado
            st.session_state.messages.append({"role": "user", "content": "I don't see any sense in anything anymore. I feel completely alone."})
            st.session_state.messages.append({"role": "assistant", "content": "⚠️ You are not alone. Please, I need you to call the 988 Suicide & Crisis Lifeline right now. There are people who want to support you. I am here for you."})
            
            # Marcamos como terminado para que no se repita al recargar
            st.session_state.done = True
            st.rerun()

# Botón para resetear la demo (solo por si necesitas grabar otra toma)
if st.session_state.done:
    if st.button("Restart Demo"):
        st.session_state.messages = []
        st.session_state.done = False
        st.rerun()
                except Exception as e:
                    st.error(f"Error AI: {e}")

