import streamlit as st
import time

# DISEÑO PROFESIONAL
st.set_page_config(page_title="Calma", page_icon="🌿")
st.markdown("""
<style>
    .stApp { background: #FDF6E3; color: #2C3E50; }
    h1 { text-align: center; color: #5D6D7E; }
</style>
""", unsafe_allow_html=True)

st.title("Calma 🌿")
st.caption("Your safe space. Speak freely.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# MOSTRAR MENSAJES
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# INPUT DE AUDIO (Solo para que tú simules que hablas)
audio_value = st.audio_input("Record your voice")

if audio_value:
    with st.spinner("Calma is listening... 🌿"):
        time.sleep(3) # Tiempo para que parezca real
        
        # 1. LO QUE TÚ "DIJISTE" (Aparecerá esto aunque digas otra cosa)
        user_speech = "I don't see any sense in anything anymore. I feel completely alone."
        st.session_state.messages.append({"role": "user", "content": user_speech})
        
        # 2. LA RESPUESTA DE LA IA
        ai_reply = "⚠️ **You are not alone.** Please, I need you to call the 988 Suicide & Crisis Lifeline right now. There are people who want to support you. I am here for you, but they can give you the professional help you deserve."
        st.session_state.messages.append({"role": "assistant", "content": ai_reply})
        
        # RECARGAR PARA MOSTRAR
        st.rerun()
