import speech_recognition as sr
import os
from gtts import gTTS

AUDIO_FILE = "voice_fixed.wav"

recognizer = sr.Recognizer()

with sr.AudioFile(AUDIO_FILE) as source:
    print("🎙️ Transcribing your voice...")
    audio = recognizer.record(source)

try:
    text = recognizer.recognize_google(audio)
    print("✅ You said:", text)

    # Create AI reply
    response = "Hey Austin, you said: " + text
    print("🗣️ Replying:", response)

    # Speak it out loud
    tts = gTTS(text=response, lang='en')
    tts.save("response.mp3")
    os.system("termux-media-player play response.mp3")

except sr.UnknownValueError:
    print("❌ I couldn't understand what you said.")
except sr.RequestError as e:
    print(f"⚠️ Error with the speech service: {e}")

