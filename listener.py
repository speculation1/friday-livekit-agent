# listener.py
import os
import speech_recognition as sr

def speak(text):
    print("🗣️ Speaking:", text)
    os.system(f'termux-tts-speak "{text}"')

def transcribe_from_file(filename):
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 500
    recognizer.dynamic_energy_threshold = True

    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)

    try:
        print("🧠 Transcribing...")
        text = recognizer.recognize_google(audio)
        print(f"📢 You said: {text}")
        return text.lower()
    except sr.UnknownValueError:
        print("❌ Could not understand audio")
        return ""
    except sr.RequestError:
        print("❌ Google API error")
        return ""

