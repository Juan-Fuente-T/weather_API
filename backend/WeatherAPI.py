from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

@app.route('/api/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    # hacer una solicitud a la API de OpenWeatherMap
    weather_response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid=097cb4956829efc4877aa5dd20140f59')
    weather = weather_response.json()
    # convertir el pronóstico del tiempo a texto
    forecast_text = f'El pronóstico del tiempo para {city} es: {weather["weather"][0]["description"]}.'
    # reformular el pronóstico del tiempo con la API de TextCortex
    textcortex_url = "https://textcortex.com/api/v1/generate_text/"
    textcortex_payload = {
        "prompt": forecast_text,
        "category": "Autocompletar",
        "language": "es",
        "length": 2,
        "creative_scale": 0.7,
        "token": "TU_TOKEN_DE_TEXTCORTEX"
    }
    textcortex_headers = {
        'Content-Type': 'application/json'
    }
    try:
        textcortex_response = requests.request("POST", textcortex_url, headers=textcortex_headers, data=json.dumps(textcortex_payload))
        textcortex_response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        return jsonify({"error": f"Error al hacer la solicitud a la API de TextCortex: {err}"})
    reformulated_forecast = textcortex_response.json()["generated_text"]
    return {'forecast': reformulated_forecast}

"""# backend en Python con Flask
from flask import Flask, request
import requests
from ibm_watson import TextToSpeechV1, LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

app = Flask(__name__)

# autenticar con la API de IBM Watson Text to Speech
authenticator = IAMAuthenticator('YOUR_IBM_WATSON_API_KEY')
text_to_speech = TextToSpeechV1(authenticator=authenticator)
text_to_speech.set_service_url('YOUR_IBM_WATSON_URL')

# autenticar con la API de IBM Watson Language Translator
authenticator = IAMAuthenticator('YOUR_IBM_WATSON_API_KEY')
language_translator = LanguageTranslatorV3(version='2018-05-01', authenticator=authenticator)
language_translator.set_service_url('YOUR_IBM_WATSON_URL')

@app.route('/api/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    # hacer una solicitud a la API de OpenWeatherMap
    weather_response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid=097cb4956829efc4877aa5dd20140f59')
    weather = weather_response.json()
    # convertir el pronóstico del tiempo a texto
    forecast_text = f'El pronóstico del tiempo para {city} es: {weather["weather"][0]["description"]}.'
    # reformular el pronóstico del tiempo con la API de DeepAI Text Generation
    deepai_response = requests.post(
        'https://api.deepai.org/api/text-generator',
        data={
            'text': forecast_text,
        },
        headers={'api-key': 'YOUR_DEEPAI_API_KEY'}
    )
    reformulated_forecast = deepai_response.json()["output"]
    # traducir el texto reformulado a otro idioma con la API de IBM Watson Language Translator
    translation = language_translator.translate(text=reformulated_forecast, model_id='en-es').get_result()
    translated_text = translation['translations'][0]['translation']
    # convertir el texto traducido a voz con la API de IBM Watson Text to Speech
    voice = text_to_speech.synthesize(translated_text, accept='audio/wav').get_result().content
    return {'voice': voice}"""