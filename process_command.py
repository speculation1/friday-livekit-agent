# process_command.py
import requests
import json
import os
import random
import edge_tts

NEWS_API_KEY = "e00594c5f6841ae896d0c3a103c5a48"
GEMINI_API_KEY = "AIzaSyCVVTKLY--XHu263TPp1v0a40q_jYkYa5U"

async def speak(text):
    print("🗣️ Speaking...")
    communicate = edge_tts.Communicate(text, voice="en-GB-LibbyNeural")
    await communicate.save("response.mp3")
    os.system("termux-media-player play response.mp3")

async def handle_command(command):
    command = command.lower()

    if "weather" in command:
        return "Weather is currently unavailable until we connect a weather API."

    elif "news" in command:
        try:
            url = f"https://newsapi.org/v2/top-headlines?country=ng&apiKey={NEWS_API_KEY}"
            response = requests.get(url)
            data = response.json()
            if "articles" in data and data["articles"]:
                top_news = data["articles"][0]["title"]
                return f"Here is the top news: {top_news}"
            else:
                return "Sorry, I couldn't find any news at the moment."
        except Exception as e:
            return f"Failed to fetch news: {str(e)}"

    elif "joke" in command:
        jokes = [
            "Why don’t scientists trust atoms? Because they make up everything!",
            "Why did the computer go to therapy? It had too many bytes of emotional baggage.",
            "Why did the scarecrow get promoted? He was outstanding in his field."
        ]
        return random.choice(jokes)

    elif "bible" in command:
        return "The Bible says in John 3:16: For God so loved the world, that He gave His only begotten Son."

    elif "who is" in command or "what is" in command:
        try:
            question = command
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
            payload = {
                "contents": [{"parts": [{"text": question}]}]
            }
            headers = {"Content-Type": "application/json"}
            response = requests.post(url, data=json.dumps(payload), headers=headers)
            output = response.json()["candidates"][0]["content"]["parts"][0]["text"]
            return output
        except Exception as e:
            return "Sorry, I couldn't answer that right now."

    elif "hello" in command or "hi" in command:
        return "Hello Austin! How can I assist you now?"

    else:
        return "Sorry, I couldn't process that right now."

