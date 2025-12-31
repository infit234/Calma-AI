import streamlit as st
from google import genai
from google.genai import types
from elevenlabs.client import ElevenLabs

# ==========================================
# 🔐 ZONA DE LLAVES
# ==========================================
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
ELEVENLABS_API_KEY = st.secrets["ELEVENLABS_API_KEY"]
# ==========================================

# 1. CEREBRO
client_google = genai.Client(api_key=GOOGLE_API_KEY)

SYSTEM_INSTRUCTIONS = """
You are 'Calma', a warm, compassionate emotional support AI.
1. Speak ONLY in English.
2. Be empathetic and concise (2-3 sentences).
3. If suicide/self-harm is mentioned, output ONLY: "CRISIS_ALERT"
"""

# 2. VOZ (Ahora soporta cambio de identidad)
client_eleven = ElevenLabs(api_key=ELEVENLABS_API_KEY)

# IDs de Voz
VOICE_RACHEL = "21m00Tcm4TlvDq8ikWAM" # Calma
VOICE_ADAM = "pNInz6obpgDQGcFmaJgB"   # Serio/Crisis

def generate_audio(text, voice_id):
    try:
        audio_stream = client_eleven.text_to_speech.convert(
            text=text,
            voice_id=voice_id, # Aquí usamos la voz dinámica
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128"
        )
        return audio_stream
    except Exception as e:
        st.error(f"Voice Error: {e}")
        return None

def transcribe_audio(audio_file):
    try:
        audio_bytes = audio_file.read()
        response = client_google.models.generate_content(
            model='gemini-2.5-flash-lite', 
            contents=[
                types.Part.from_bytes(data=audio_bytes, mime_type="audio/wav"),
                "Transcribe exactly what is said in this audio. Do not add anything else."
            ]
        )
        return response.text
    except Exception:
        try:
             response = client_google.models.generate_content(
                model='gemini-2.0-flash-lite-preview-02-05',
                contents=[
                    types.Part.from_bytes(data=audio_bytes, mime_type="audio/wav"),
                    "Transcribe..."
                ]
            )
             return response.text
        except:
            st.error("Error AI. Check Quota.")
            return None

# 3. DISEÑO
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

# 4. INTERFAZ
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
# 🎤 GRABACIÓN INTELIGENTE
# ==========================================
audio_value = st.audio_input("Record voice")

if audio_value:
    if audio_value == st.session_state.last_processed_audio:
        pass 
    else:
        st.session_state.last_processed_audio = audio_value
        
        with st.spinner("Thinking... 🌿"):
            transcript = transcribe_audio(audio_value)
            
            if transcript:
                # 1. Guardar usuario
                st.session_state.messages.append({"role": "user", "content": transcript})
                with st.chat_message("user"):
                    st.markdown(transcript)
                
                try:
                    # 2. Generar texto
                    response = client_google.models.generate_content(
                        model='gemini-2.5-flash-lite',
                        contents=transcript,
                        config=types.GenerateContentConfig(
                            system_instruction=SYSTEM_INSTRUCTIONS
                        )
                    )
                    
                    reply_text = response.text
                    
                    # 3. LÓGICA DE VOZ (Aquí ocurre la magia)
                    current_voice = VOICE_RACHEL # Por defecto: Rachel
                    
                    if "CRISIS_ALERT" in reply_text:
                        reply_text = "⚠️ You are not alone. Please call 988 immediately."
                        current_voice = VOICE_ADAM # Cambio a voz seria (Adam)
                    
                    # 4. Generar audio con la voz seleccionada
                    audio_bytes = b""
                    audio_stream = generate_audio(reply_text, current_voice)
                    if audio_stream:
                        for chunk in audio_stream:
                            audio_bytes += chunk
                    
                    # 5. Guardar y mostrar respuesta
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": reply_text,
                        "audio": audio_bytes
                    })

                    with st.chat_message("assistant"):
                        st.markdown(reply_text)
                        if audio_bytes:
                            st.audio(audio_bytes, format="audio/mp3", autoplay=True)

                except Exception as e:
                    st.error(f"Error AI: {e}")
