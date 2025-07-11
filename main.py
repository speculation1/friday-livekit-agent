# livekit_agent.py
import os
import json
import random
import asyncio
import requests
import edge_tts
from livekit import rtc
from process_command import handle_command, speak as tts_speak

# Load env variables or hardcode for now
LIVEKIT_URL = os.getenv("LIVEKIT_URL", "wss://javis-1-dynyqa10.livekit.cloud")
LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY", "APILdQrt8irrokn")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET", "3oSrv9hsA2MYMs8ZeGeA2QmazDBcryKqin1w6U8HnOF")
ROOM_NAME = "friday-room"
PARTICIPANT_NAME = "FridayBot"
WAKE_WORDS = ["hey friday", "hi friday", "friday"]

async def handle_audio_stream(room: rtc.Room):
    print("🎧 Friday is listening via LiveKit...")

    async for track in room.audio_tracks():
        async for frame in track.frames():
            audio_path = "temp_input.wav"
            with open(audio_path, "wb") as f:
                f.write(frame.payload)

            # Transcribe
            try:
                from speech_recognition import Recognizer, AudioFile
                recognizer = Recognizer()
                with AudioFile(audio_path) as source:
                    audio = recognizer.record(source)
                text = recognizer.recognize_google(audio)
                print(f"🗣️ Heard: {text}")
            except:
                continue

            if any(w in text.lower() for w in WAKE_WORDS):
                await tts_speak("Yes, I’m here. What can I do for you?")

                # Listen again for the command
                print("🎧 Listening for command...")
                async for next_frame in track.frames():
                    with open(audio_path, "wb") as f:
                        f.write(next_frame.payload)
                    try:
                        with AudioFile(audio_path) as source:
                            audio = recognizer.record(source)
                        command = recognizer.recognize_google(audio)
                        print(f"📥 Command: {command}")
                        response = await handle_command(command)
                        await tts_speak(response)
                        break
                    except:
                        continue

async def connect_and_run():
    print("🔌 Connecting to LiveKit...")
    room = await rtc.connect(
        LIVEKIT_URL,
        rtc.AccessToken(
            LIVEKIT_API_KEY,
            LIVEKIT_API_SECRET,
            identity=PARTICIPANT_NAME,
            name=PARTICIPANT_NAME
        ).to_jwt(),
        ROOM_NAME
    )
    await handle_audio_stream(room)

if __name__ == "__main__":
    asyncio.run(connect_and_run())

