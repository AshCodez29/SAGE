import os
import pvporcupine
import pyaudio
import struct
from dotenv import load_dotenv

load_dotenv()

from core.llm import think
from core.stt import transcribe
from core.tts import speak

def main():
    porcupine = pvporcupine.create(
        access_key=os.getenv("PORCUPINE_API_KEY"),
        keywords=["jarvis"]  # closest built-in to "SAGE" for now
    )

    pa = pyaudio.PyAudio()
    stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length
    )

    print("SAGE is listening... say 'Hey Jarvis' to wake me")
    speak("SAGE online. How can I help you?")

    while True:
        raw = stream.read(porcupine.frame_length, exception_on_overflow=False)
        pcm = struct.unpack_from("h" * porcupine.frame_length, raw)

        result = porcupine.process(pcm)

        if result >= 0:
            print("Wake word detected! Listening...")
            speak("Yes?")

            text = transcribe()       # mic → whisper → text
            print(f"You said: {text}")

            if text:
                response = think(text) # text → GPT → response
                print(f"SAGE: {response}")
                speak(response)        # response → ElevenLabs → audio

if __name__ == "__main__":
    main()
