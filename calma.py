<!-- end list -->

import streamlit as st

import time # Para simular que piensa

from elevenlabs.client import ElevenLabs



# ==========================================

# 🔐 SOLO NECESITAS LA LLAVE DE ELEVENLABS

# ==========================================

ELEVENLABS_API_KEY = st.secrets["ELEVENLABS_API_KEY"]

# ==========================================



client_eleven = ElevenLabs(api_key=ELEVENLABS_API_KEY)



# IDs de Voz

VOICE_RACHEL = "21m00Tcm4TlvDq8ikWAM" 

VOICE_ADAM = "pNInz6obpgDQGcFmaJgB"   



def generate_audio(text, voice_id):

    try:

        audio_stream = client_eleven.text_to_speech.convert(

            text=text,

            voice_id=voice_id, 

            model_id="eleven_multilingual_v2",

            output_format="mp3_44100_128"

        )

        return audio_stream

    except Exception as e:

        st.error(f"Voice Error: {e}")

        return None



# DISEÑO IDÉNTICO AL ORIGINAL

st.set_page_config(page_title="Calma", page_icon="🌿", layout="centered")



st.markdown("""

<style>

    .stApp {

        background: linear-gradient(180deg, #FDF6E3 0%, #F5E6CA 100%);

        color: #2C3E50;

    }

    h1 {

        font-family: 'Helvetica Neue', sans-serif;

        color: #5D6D7E !important;

        font-weight: 300;

        text-align: center;

        margin-top: -20px;

    }

    p { text-align: center; color: #7F8C8D; }

    .stChatMessage {

        background-color: rgba(255,255,255,0.9);

        border-radius: 15px;

        border: none;

        box-shadow: 0 2px 5px rgba(0,0,0,0.05);

    }

    .stAudioInput {

        position: fixed;

        bottom: 50px;           

        left: 50%;              

        transform: translateX(-50%);

        width: 70% !important;  

        z-index: 9999;

        background-color: white;

        padding: 15px;

        border-radius: 40px;    

        box-shadow: 0 10px 30px rgba(0,0,0,0.15);

        border: 1px solid #ddd;

    }

    .block-container { padding-bottom: 180px; }

    header {visibility: hidden;}

    footer {visibility: hidden;}

</style>

""", unsafe_allow_html=True)



st.title("Calma 🌿")

st.caption("Your safe space. I'm listening.")



if "messages" not in st.session_state:

    st.session_state.messages = []

if "last_processed_audio" not in st.session_state:

    st.session_state.last_processed_audio = None



# Mostrar Historial

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if "audio" in message:

            st.audio(message["audio"], format="audio/mp3", start_time=0)



# ==========================================

# 🎬 MODO SIMULACIÓN PARA VIDEO

# ==========================================

audio_value = st.audio_input("Record voice")



if audio_value:

    if audio_value == st.session_state.last_processed_audio:

        pass 

    else:

        st.session_state.last_processed_audio = audio_value

        

        with st.spinner("Thinking... 🌿"):

            time.sleep(2) # Fingimos que piensa 2 segundos

            

            # 1. TEXTO DEL USUARIO (PRE-FABRICADO PARA EL VIDEO)

            # Aunque digas "Hola", aparecerá esto:

            transcript = "I don't see any sense in anything anymore. I am thinking of ending everything."

            

            # Guardamos y mostramos lo que "dijiste"

            st.session_state.messages.append({"role": "user", "content": transcript})

            with st.chat_message("user"):

                st.markdown(transcript)

            

            # 2. RESPUESTA DE LA IA (PRE-FABRICADA DE CRISIS)

            reply_text = "⚠️ You are not alone. Please call 988 immediately. I am connecting you with resources now."

            

            # 3. GENERAMOS AUDIO CON VOZ DE ADAM (Crisis)

            # Como ElevenLabs SÍ funciona, esto se escuchará real

            audio_bytes = b""

            audio_stream = generate_audio(reply_text, VOICE_ADAM)

            

            if audio_stream:

                for chunk in audio_stream:

                    audio_bytes += chunk

            

            st.session_state.messages.append({

                "role": "assistant", 

                "content": reply_text,

                "audio": audio_bytes

            })



            with st.chat_message("assistant"):

                st.markdown(reply_text)

                if audio_bytes:

                    st.audio(audio_bytes, format="audio/mp3", autoplay=True)

