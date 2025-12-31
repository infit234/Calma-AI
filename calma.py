import streamlit as st
from google import genai
from google.genai import types
from elevenlabs.client import ElevenLabs
from streamlit_mic_recorder import mic_recorder
import io

# ==========================================
# 🔐 API KEYS ZONE
# ==========================================
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
ELEVENLABS_API_KEY = st.secrets["ELEVENLABS_API_KEY"]
# ==========================================

# 1. BRAIN SETUP
client_google = genai.Client(api_key=GOOGLE_API_KEY)

SYSTEM_INSTRUCTIONS = """
You are 'Calma', a warm, compassionate emotional support AI.
1. Speak ONLY in English.
2. Be empathetic and concise (2-3 sentences).
3. If the input is audio, listen carefully.
4. If suicide/self-harm is mentioned, output ONLY: "CRISIS_ALERT"
"""

# 2. VOICE SETUP
client_eleven = ElevenLabs(api_key=ELEVENLABS_API_KEY)

def generate_audio(text):
    try:
        audio_stream = client_eleven.text_to_speech.convert(
            text=text,
            voice_id="21m00Tcm4TlvDq8ikWAM", 
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128"
        )
        return audio_stream
    except Exception as e:
        st.error(f"Voice Error: {e}")
        return None

def transcribe_audio(audio_bytes):
    """Uses Gemini to transcribe the user's voice audio"""
    try:
        # CORRECCIÓN AQUÍ: Usamos el modelo comodín que sí te funciona
        response = client_google.models.generate_content(
            model='gemini-flash-latest', 
            contents=[
                types.Part.from_bytes(data=audio_bytes, mime_type="audio/wav"),
                "Transcribe exactly what is said in this audio. Do not add anything else."
            ]
        )
        return response.text
    except Exception as e:
        st.error(f"Transcription Error: {e}")
        return None

# 3. UI DESIGN
st.set_page_config(page_title="Calma", page_icon="🌿", layout="centered")

st.markdown("""
<style>
    .stApp { background-color: #FDF6E3; color: #2C3E50; }
    .stTextInput > div > div > input { background-color: #ffffff; color: #2C3E50; border-radius: 20px; }
    h1 { color: #5D6D7E; font-family: 'Helvetica Neue', sans-serif; }
    .stChatMessage { background-color: #ffffff; border-radius: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
    button { border-radius: 50% !important; }
</style>
""", unsafe_allow_html=True)

st.title("🌿 Calma")
st.caption("Press the microphone to speak, or type below.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Show History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "audio" in message:
            st.audio(message["audio"], format="audio/mp3", start_time=0)

# ==========================================
# 🎤 INPUT AREA
# ==========================================
col1, col2 = st.columns([1, 8])

input_text = None

# Microphone Input
with col1:
    st.write("🎙️")
    audio_data = mic_recorder(
        start_prompt="Start",
        stop_prompt="Stop",
        just_once=True,
        key='recorder',
        format="wav"
    )

# Text Input
with col2:
    text_prompt = st.chat_input("...or type here")

# LOGIC
user_input = None

if audio_data and "bytes" in audio_data:
    with st.spinner("Listening to you..."):
        transcript = transcribe_audio(audio_data['bytes'])
        if transcript:
            user_input = transcript

elif text_prompt:
    user_input = text_prompt

# PROCESS
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Brain processing
                response = client_google.models.generate_content(
                    model='gemini-flash-latest', 
                    contents=user_input,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_INSTRUCTIONS
                    )
                )
                
                reply_text = response.text
                
                if "CRISIS_ALERT" in reply_text:
                    reply_text = "⚠️ You are not alone. Please call 988."
                
                st.markdown(reply_text)
                
                # Voice generation
                audio_bytes = b""
                audio_stream = generate_audio(reply_text)
                if audio_stream:
                    for chunk in audio_stream:
                        audio_bytes += chunk
                    st.audio(audio_bytes, format="audio/mp3", autoplay=True)
                
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": reply_text,
                    "audio": audio_bytes
                })

            except Exception as e:
                st.error(f"Error: {e}")
