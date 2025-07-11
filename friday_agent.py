import os
import requests
import sounddevice as sd
import scipy.io.wavfile as wav
import tempfile

# Replace with your actual Replit backend URL
BACKEND_URL = "https://friday-livekit-agent.speculation1.repl.co/speak/?text="

def record_voice(duration=5, fs=44100):
    print("🎙️ Speak now...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    wav.write(temp_file.name, fs, recording)
    return temp_file.name

def main():
    user_input = input("🗣️ What do you want to say to Friday? → ")
    url = BACKEND_URL + requests.utils.quote(user_input)
    print("🤖 Sending to Friday...")
    response = requests.get(url)
    if response.ok:
        print("✅ Response received.")
    else:
        print("❌ Something went wrong:", response.text)

if __name__ == "__main__":
    main()

