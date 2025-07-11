from fastapi import FastAPI
from pydantic import BaseModel
import os

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Friday LiveKit + Gemini backend is running."}

@app.post("/ask/")
def ask_gemini(prompt: str):
    return {"response": f'Gemini would say something about: {prompt}'}

