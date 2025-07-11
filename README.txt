# Chatterbox AI Assistant (Simplified for Termux)

## Installation Steps

1. Open Termux and run:

   pkg update -y
   pkg install python termux-api -y
   pip install --upgrade pip setuptools wheel
   pip install -r requirements.txt

2. Run the assistant:

   uvicorn main:app --reload --host 0.0.0.0 --port 8000

3. Visit in your browser:
   http://127.0.0.1:8000

4. Test the voice API:
   http://127.0.0.1:8000/speak/?text=Hello%20there

*No SpeechRecognition or heavy libraries needed.*
