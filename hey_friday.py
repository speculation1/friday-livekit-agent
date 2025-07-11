import os
import time
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound

WAKE_WORDS = ["hey friday", "hi friday", "friday"]
WAKE_AUDIO = "wake_raw.amr"
CLEAN_AUDIO = "wake_final.wav"
RESPONSE_FILE = "response.mp3"
RECORD_DURATION = 7

def record_audio():
    print("🎙️ Recording...")
    os.system(f"termux-microphone-record -f {WAKE_AUDIO} -l {RECORD_DURATION}")
    time.sleep(RECORD_DURATION + 1)

def boost_and_clean_audio():
    print("🔄 Boosting & Cleaning audio...")
    os.system(
        f"ffmpeg -y -i {WAKE_AUDIO} -af 'volume=10.0, highpass=f=200, lowpass=f=3000, afftdn' {CLEAN_AUDIO}"
    )
    print("✅ Conversion successful.")

def transcribe_audio():
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 500
    recognizer.dynamic_energy_threshold = True

    with sr.AudioFile(CLEAN_AUDIO) as source:
        audio = recognizer.record(source)

    try:
        print("🧠 Transcribing...")
        text = recognizer.recognize_google(audio)
        print(f"🗣️ You said: {text}")
        return text.lower()
    except sr.UnknownValueError:
        print("❌ Could not understand audio")
        return ""
    except sr.RequestError:
        print("❌ Google API error")
        return ""

def respond(message):
    tts = gTTS(text=message, lang='en')
    tts.save(RESPONSE_FILE)
    playsound(RESPONSE_FILE)

def main():
    print("⏳ Waiting for wake word: 'Hey Friday'...")
    record_audio()
    boost_and_clean_audio()
    transcription = transcribe_audio()

    if any(wake in transcription for wake in WAKE_WORDS):
        print("✅ Wake word detected!")
        respond("Hello, I'm Friday. How can I help you?")
    else:
        print("⏳ Wake word not detected. Please try again.")

if __name__ == "__main__":
    main()

