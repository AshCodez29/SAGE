import os

from elevenlabs import play
from elevenlabs.client import ElevenLabs

client = None

# Pick a voice from elevenlabs.io/voice-library
# "Rachel" is calm and clear - good default for SAGE
VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # Rachel - swap with any voice you like


def speak(text: str):
    global client
    if client is None:
        api_key = os.getenv("ELEVENLABS_API_KEY") or os.getenv("ELEVENLABS_API")
        if not api_key:
            raise RuntimeError("ELEVENLABS_API_KEY is missing. Set ELEVENLABS_API_KEY or ELEVENLABS_API in your environment or .env file.")
        client = ElevenLabs(api_key=api_key)

    print(f"[SAGE speaking]: {text}")
    audio = client.text_to_speech.convert(
        voice_id=VOICE_ID,
        text=text,
        model_id="eleven_multilingual_v2",  # handles Hindi/Hinglish
        output_format="mp3_44100_128",
    )
    play(audio)
