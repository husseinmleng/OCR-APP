import os
import csv
import pytesseract
from PIL import Image
from flask import Flask, request, jsonify,send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)


@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/extract_text', methods=['POST'])
def extract_text():
    # Check if the post request has the file part
    if 'image' not in request.files:
        return jsonify({'message': 'No file part in the request'}), 400

    file = request.files['image']

    # If no file is selected
    if file.filename == '':
        return jsonify({'message': 'No file selected for uploading'}), 400

    if file and (file.filename.endswith('.jpg') or file.filename.endswith('.png')):
        # Open the image using PIL
        image = Image.open(file)

        # Perform OCR using pytesseract
        text = pytesseract.image_to_string(image)

        # Extract text and numbers using regular expressions
        import re
        text_numbers = re.findall(r'\d+|\b\w+\b', text)
        text_numbers = [x.strip() for x in text_numbers]
        text_numbers = [x for x in text_numbers if len(x) > 0]

        # Return a JSON response with the extracted text
        return jsonify({'extracted_text': ' '.join(text_numbers)})

    else:
        return jsonify({'message': 'Allowed file types are .jpg, .png'}), 400

if __name__ == '__main__':
    app.run(debug=True)
