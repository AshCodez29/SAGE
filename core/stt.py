import os
import tempfile
import wave

import pyaudio
import whisper

model = whisper.load_model("base")  # or "small" for better accuracy

RATE = 16000
CHANNELS = 1
CHUNK = 1024
SECONDS = 5  # how long SAGE listens after wake word


def transcribe() -> str:
    pa = pyaudio.PyAudio()
    stream = pa.open(
        format=pyaudio.paInt16,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
    )

    print("Recording...")
    frames = [stream.read(CHUNK) for _ in range(0, int(RATE / CHUNK * SECONDS))]
    stream.stop_stream()
    stream.close()
    pa.terminate()

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        with wave.open(f, "wb") as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(pa.get_sample_size(pyaudio.paInt16))
            wf.setframerate(RATE)
            wf.writeframes(b"".join(frames))
        tmp_path = f.name

    try:
        result = model.transcribe(tmp_path, language=None)  # auto-detect Hindi/English
        return result["text"].strip()
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
import whisper
import pyaudio
import wave
import tempfile

model = whisper.load_model("base")  # or "small" for better accuracy

RATE     = 16000
CHANNELS = 1
CHUNK    = 1024
SECONDS  = 5   # how long SAGE listens after wake word

def transcribe() -> str:
    pa = pyaudio.PyAudio()
    stream = pa.open(format=pyaudio.paInt16, channels=CHANNELS,
                     rate=RATE, input=True, frames_per_buffer=CHUNK)

    print("Recording...")
    frames = [stream.read(CHUNK) for _ in range(0, int(RATE / CHUNK * SECONDS))]
    stream.stop_stream(); stream.close(); pa.terminate()

    # save to temp wav file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        wf = wave.open(f, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(pa.get_sample_size(pyaudio.paInt16))
        wf.setframerate(RATE)
        wf.writeframes(b"".join(frames))
        tmp_path = f.name

    result = model.transcribe(tmp_path, language=None)  # None = auto-detect Hindi/English
    return result["text"].strip()
