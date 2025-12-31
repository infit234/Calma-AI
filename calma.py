import streamlit as st
from google import genai
from google.genai import types
from elevenlabs.client import ElevenLabs

# ==========================================
# 🔐 API KEYS ZONE
# ==========================================
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
ELEVENLABS_API_KEY = st.secrets["ELEVENLABS_API_KEY"]
# ==========================================

# 1. BRAIN SETUP (English Personality)
client_google = genai.Client(api_key=GOOGLE_API_KEY)

# We define a richer, more emotional persona
SYSTEM_INSTRUCTIONS = """
You are 'Calma', a warm, compassionate, and gentle emotional support AI companion.
Your goal is to make the user feel heard, validated, and safe.

GUIDELINES:
1. LANGUAGE: Speak ONLY in English.
2. TONE: Use a soft, conversational, and empathetic tone. Avoid robotic phrasing like "I understand." Instead use: "I'm so sorry you're going through this," "I hear you," or "That sounds really heavy."
3. LENGTH: You can use 2-3 sentences to express empathy fully, but keep it conversational.
4. SAFETY: If the user mentions self-harm or suicide, drop the persona immediately and output EXACTLY: "CRISIS_ALERT"
"""

# 2. VOICE SETUP
client_eleven = ElevenLabs(api_key=ELEVENLABS_API_KEY)

def generate_audio(text):
    try:
        # Using "Rachel" (ID: 21m00Tcm4TlvDq8ikWAM) - A very calming voice
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

# 3. WARM UI DESIGN (CSS)
st.set_page_config(page_title="Calma", page_icon="🌿", layout="centered")

st.markdown("""
<style>
    /* Warm Background (Cream/Paper color) - More inviting than dark mode */
    .stApp {
        background-color: #FDF6E3;
        color: #2C3E50;
    }
    
    /* Input Box Styling */
    .stTextInput > div > div > input {
        background-color: #ffffff;
        color: #2C3E50;
        border-radius: 20px;
        border: 1px solid #D3C4A5;
    }

    /* Titles */
    h1 {
        color: #5D6D7E !important; 
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 200;
    }
    
    /* Chat Bubbles */
    .stChatMessage {
        background-color: #ffffff;
        border-radius: 15px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        color: #2C3E50; /* Dark text for readability */
    }
    
    /* User Message Specifics */
    div[data-testid="stChatMessageContent"] {
        color: #2C3E50 !important;
    }
    
    /* Spinner color */
    .stSpinner > div {
        border-top-color: #D3C4A5 !important;
    }
</style>
""", unsafe_allow_html=True)

# 4. APP INTERFACE
st.title("🌿 Calma")
st.caption("Your safe space. I'm here to listen.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "audio" in message:
            st.audio(message["audio"], format="audio/mp3", start_time=0)

# 5. INTERACTION LOGIC
if prompt := st.chat_input("Tell me what's on your mind..."):
    
    # Save User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Response
    with st.chat_message("assistant"):
        with st.spinner("Listening..."):
            try:
                # Using the robust model 'gemini-flash-latest'
                response = client_google.models.generate_content(
                    model='gemini-flash-latest', 
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_INSTRUCTIONS
                    )
                )
                
                reply_text = response.text
                
                # Safety Check (English)
                if "CRISIS_ALERT" in reply_text:
                    reply_text = "⚠️ You are not alone. Please call the National Suicide Prevention Lifeline: 988 or text HOME to 741741."
                
                st.markdown(reply_text)
                
                # Generate Audio
                audio_bytes = b""
                audio_stream = generate_audio(reply_text)
                
                if audio_stream:
                    for chunk in audio_stream:
                        audio_bytes += chunk
                    st.audio(audio_bytes, format="audio/mp3", autoplay=True)
                
                # Save Assistant Message
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": reply_text,
                    "audio": audio_bytes
                })

            except Exception as e:
                st.error(f"Error: {e}")