 
# Import necessary libraries
from flask import Flask, render_template, request, redirect, url_for
from google.cloud import speech

# Create a Flask app
app = Flask(__name__)

# Define the routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stt', methods=['POST'])
def stt():
    # Get the audio data from the request
    audio_data = request.files['audio_data']

    # Create a Speech client
    client = speech.SpeechClient()

    # Configure the request
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US'
    )

    # Send the audio data to the Speech client
    response = client.recognize(config=config, audio=audio_data)

    # Get the transcription
    transcription = response.results[0].alternatives[0].transcript

    # Return the transcription
    return transcription

@app.route('/tts', methods=['POST'])
def tts():
    # Get the text from the request
    text = request.form['text']

    # Create a Speech client
    client = speech.SpeechClient()

    # Configure the request
    config = speech.SynthesisInputConfig(text=text)

    # Send the text to the Speech client
    response = client.synthesize_speech(config=config)

    # Get the audio data
    audio_data = response.audio_content

    # Return the audio data
    return audio_data

# Run the app
if __name__ == '__main__':
    app.run()
