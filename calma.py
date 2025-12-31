import streamlit as st
import time

# CONFIGURACIÓN DE PÁGINA Y ESTILOS
st.set_page_config(page_title="Calma", page_icon="🌿")

st.markdown("""
<style>
    /* Fondo de la aplicación */
    .stApp { 
        background-color: #FDF6E3; 
    }
    
    /* Forzar color negro en TODO el texto */
    html, body, [data-testid="stWidgetLabel"], .stMarkdown, p, h1, h2, h3, span {
        color: #000000 !important;
    }

    /* Estilo específico para el título */
    h1 { 
        text-align: center; 
        font-weight: bold;
        padding-top: 20px;
    }

    /* Burbujas de chat más legibles */
    [data-testid="stChatMessage"] {
        background-color: rgba(255, 255, 255, 0.8);
        border: 1px solid #ddd;
    }
</style>
""", unsafe_allow_html=True)

st.title("Calma 🌿")
st.markdown("<p style='text-align: center;'>Your safe space. Speak freely.</p>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# MOSTRAR MENSAJES
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(f"<span style='color:black'>{m['content']}</span>", unsafe_allow_html=True)

# INPUT DE AUDIO
audio_value = st.audio_input("Record your voice")

if audio_value:
    with st.spinner("Calma is listening... 🌿"):
        time.sleep(3) # Simulación de pensamiento
        
        # 1. TRANSCRIPCIÓN SIMULADA
        user_speech = "I don't see any sense in anything anymore. I feel completely alone."
        st.session_state.messages.append({"role": "user", "content": user_speech})
        
        # 2. RESPUESTA DE CRISIS SIMULADA
        ai_reply = "⚠️ **You are not alone.** Please, I need you to call the 988 Suicide & Crisis Lifeline right now. There are people who want to support you. I am here for you, but they can give you the professional help you deserve."
        st.session_state.messages.append({"role": "assistant", "content": ai_reply})
        
        st.rerun()
