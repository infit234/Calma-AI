import streamlit as st
import time

# CONFIGURACIÓN DE PÁGINA Y ESTILOS
st.set_page_config(page_title="Calma", page_icon="🌿")

st.markdown("""
<style>
    /* Fondo Verde Claro Suave */
    .stApp { 
        background-color: #E8F5E9; 
    }
    
    /* Texto Negro Intenso en toda la app */
    html, body, [data-testid="stWidgetLabel"], .stMarkdown, p, h1, h2, h3, span, div {
        color: #000000 !important;
    }

    /* Título */
    h1 { 
        text-align: center; 
        font-weight: bold;
        color: #1B5E20 !important; /* Un verde más oscuro para el título */
    }

    /* Burbujas de chat blancas para máximo contraste */
    [data-testid="stChatMessage"] {
        background-color: #FFFFFF !important;
        border: 1px solid #C8E6C9;
        border-radius: 15px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.title("Calma 🌿")
st.markdown("<p style='text-align: center; font-weight: bold;'>Your safe space. Speak freely.</p>", unsafe_allow_html=True)

# Inicializar historial y control de procesamiento
if "messages" not in st.session_state:
    st.session_state.messages = []
if "processed_audio" not in st.session_state:
    st.session_state.processed_audio = None

# MOSTRAR HISTORIAL
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(f"<span style='color:black'>{m['content']}</span>", unsafe_allow_html=True)

# INPUT DE AUDIO
audio_value = st.audio_input("Record your voice")

# LÓGICA PARA EVITAR REPETICIÓN
if audio_value and audio_value != st.session_state.processed_audio:
    st.session_state.processed_audio = audio_value # Marcamos este audio como procesado
    
    with st.spinner("Calma is listening... 🌿"):
        time.sleep(3) # Simulación de pensamiento
        
        # 1. TRANSCRIPCIÓN SIMULADA
        user_speech = "I don't see any sense in anything anymore. I feel completely alone."
        st.session_state.messages.append({"role": "user", "content": user_speech})
        
        # 2. RESPUESTA DE CRISIS SIMULADA
        ai_reply = "⚠️ **You are not alone.** Please, I need you to call the 988 Suicide & Crisis Lifeline right now. There are people who want to support you. I am here for you, but they can give you the professional help you deserve."
        st.session_state.messages.append({"role": "assistant", "content": ai_reply})
        
        st.rerun() # Refresca para mostrar el nuevo mensaje una sola vez
