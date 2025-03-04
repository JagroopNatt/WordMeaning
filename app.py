from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    meaning = None
    example = None
    word = None
    phonetics = None
    part_of_speech = None
    synonyms = None
    antonyms = None
    error_message = None

    if request.method == 'POST':
        word = request.form['word']
        try:
            response = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}')
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                meanings = data[0].get('meanings', [])
                if meanings:
                    definitions = meanings[0].get('definitions', [])
                    if definitions:
                        meaning = definitions[0].get('definition', 'No meaning found.')
                        example = definitions[0].get('example', 'No example found.')
                        phonetics = data[0].get('phonetics', [{}])[0].get('text', 'No phonetics found.')
                        part_of_speech = meanings[0].get('partOfSpeech', 'No part of speech found.')
                        synonyms = ', '.join(meanings[0].get('synonyms', ['No synonyms found.']))
                        antonyms = ', '.join(meanings[0].get('antonyms', ['No antonyms found.']))
        except requests.exceptions.RequestException as e:
            error_message = str(e)

    return render_template('index.html', meaning=meaning, example=example, word=word, phonetics=phonetics, 
                           part_of_speech=part_of_speech, synonyms=synonyms, antonyms=antonyms, 
                           error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)
