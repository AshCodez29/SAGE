import os
from dotenv import load_dotenv
from core.stt import transcribe
from core.llm import think
from core.tts import speak

load_dotenv()


def say(text: str) -> None:
    if os.getenv("ELEVENLABS_API_KEY") or os.getenv("ELEVENLABS_API"):
        speak(text)
    else:
        print(f"[SAGE]: {text}")

def main():
    say("SAGE online. Press Enter anytime to talk to me.")
    print("SAGE is ready. Press Enter to speak, Ctrl+C to quit.")

    while True:
        input()  # just press Enter to activate
        print("Listening...")
        say("Yes?")

        text = transcribe()
        print(f"You said: {text}")

        if text:
            response = think(text)
            print(f"SAGE: {response}")
            say(response)
#h fiufgrfqryb6u
if __name__ == "__main__":
    main()
