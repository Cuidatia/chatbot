from flask import Flask, jsonify, request
import requests
import json
from flask_cors import CORS
import speech_recognition as sr
app = Flask(__name__)
CORS(app)

lenguaje = 'es-ES'
# mixer.init()
r = sr.Recognizer()

headers = {
    'content-type': 'application/json',
    'x-api-key': '985e1723-86f3-4311-9805-2e71b19b2b1c'
}

@app.route('/reconocer-voz', methods=['GET'])
def reconocer_voz():
    with sr.Microphone() as voz:
        audio = r.listen(voz)
        
    try:
        return r.recognize_google(audio, language=lenguaje)
    except sr.UnknownValueError:
        return "No te entiendo"
    except sr.RequestError as e:
        return "Google Speech Recognition; {0}".format(e)

@app.route('/chatbot', methods=['POST'])
def chatbot_voice():
    if request.method == 'POST':
        data = request.data.decode()
        json_data = json.loads(data)
        pregunta = json_data.get('text')
        response = requests.post('https://bots.easy-peasy.ai/bot/779461bc-a712-4a7b-aed0-bfc368139eb3', headers=headers, json={
                        "message": pregunta + '. Máximo 100 palabras',
                        "history": [],
                        "stream": False,
                        })
        for linea in response.text.split('\n'):
            if not linea.strip():
                continue
            
            evento = json.loads(linea)

            if 'bot' in evento:
                mensaje_bot = evento['bot']['text']
                return mensaje_bot

if __name__ == '__main__':
    app.run(debug=True)