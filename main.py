from fastapi import FastAPI
from gtts import gTTS
import os
import random
from starlette.responses import JSONResponse
from starlette.requests import Request

app = FastAPI()

# Fun responses Friday can add to any message
funny_responses = [
    "You're awesome! Just don't forget to blink 🤪.",
    "Sure thing, but only because you asked so nicely 💅.",
    "I would do it even faster if I had hands! 😂"
]

@app.get("/")
async def root():
    """Health check endpoint."""
    return JSONResponse({"message": "Friday backend is running 🎉"})

@app.get("/speak/")
async def speak(request: Request):
    """
    Text-to-speech endpoint.
    Example:
      /speak/?text=Hello%20Austin
    """
    text = request.query_params.get("text", "Hello")
    response = random.choice(funny_responses) + " " + text

    tts = gTTS(text=response, lang='en', slow=False)
    tts.save("response.mp3")

    # Play audio in the background (non-blocking)
    os.system("termux-media-player play response.mp3 &")
    return {"spoken": response}

