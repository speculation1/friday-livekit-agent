import os
import time
import asyncio
from listener import speak, transcribe_from_file
from process_command import handle_command, speak as speak_async

# Wake word variations
WAKE_WORDS = ["hey friday", "hi friday", "friday"]

# File names
WAKE_AUDIO = "wake_raw.amr"
WAKE_WAV = "wake_final.wav"
COMMAND_AUDIO = "command_raw.amr"
COMMAND_WAV = "command.wav"

# Record using Termux microphone and auto delete old file
def record(file, duration=7):
    if os.path.exists(file):
        os.remove(file)
    print(f"🎙️ Recording: {file}")
    os.system(f"termux-microphone-record -f {file} -l {duration}")
    time.sleep(duration + 1)

# Clean and boost audio with safe filters for 8000 Hz input
def clean_audio(input_file, output_file):
    print("🔧 Boosting & cleaning audio...")
    os.system(
        f"ffmpeg -y -i {input_file} "
        f"-af 'volume=20.0, highpass=f=100, lowpass=f=3000, afftdn=nf=-25' "
        f"{output_file}"
    )
    print("✅ Audio cleaned and ready.")

# Main assistant loop
async def main():
    print("🤖 Friday is listening for: 'Hey Friday'...")

    while True:
        # 1. Listen for wake word
        record(WAKE_AUDIO, duration=7)
        clean_audio(WAKE_AUDIO, WAKE_WAV)
        transcript = transcribe_from_file(WAKE_WAV)

        if any(wake in transcript for wake in WAKE_WORDS):
            print("✅ Wake word detected!")
            speak("Yes Austin, I'm listening.")

            # 2. Record user's command
            record(COMMAND_AUDIO, duration=8)
            clean_audio(COMMAND_AUDIO, COMMAND_WAV)
            command_text = transcribe_from_file(COMMAND_WAV)

            if command_text:
                print(f"📥 Command: {command_text}")
                response = await handle_command(command_text)
                await speak_async(response)
            else:
                speak("Sorry, I didn't catch that.")
        else:
            print("⏳ Wake word not detected. Listening again...")
        time.sleep(1)

# Run assistant
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("👋 Friday paused.")

