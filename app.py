import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
tf.get_logger().setLevel('ERROR')

from flask import Flask, request, jsonify, render_template, send_file, abort
from flask_cors import CORS
from model import predict_image
from remover import remove_background
from enhance import enhance_image
from hf_api import generate_text, caption_image
from generator import generate_image
import traceback, io

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024
CORS(app)

@app.before_request
def check_honeypot():
    if request.method == 'POST' and request.form.get('website'):
        abort(403)

# === Active pages ===
@app.route('/')
def index():
    return render_template('wip.html')

@app.route('/remover')
def remover():
    return render_template('remover.html')

@app.route('/generator')
def generator_page():
    return render_template('generator.html')

@app.route('/chat')
def chat_page():
    return render_template('chat.html')

@app.route('/caption')
def caption_page():
    return render_template('caption.html')

@app.route('/enhance')
def enhance_page():
    return render_template('enhance.html')

@app.route('/products')
def products():
    return render_template('products.html')

# === WIP pages ===
@app.route('/ocr')
@app.route('/restore')
def wip():
    return render_template('wip.html')

# === Active APIs ===
@app.route('/remove-bg', methods=['POST'])
def remove_bg():
    if 'image' not in request.files:
        return jsonify({'error': 'No image'}), 400
    try:
        data = remove_background(request.files['image'].read())
        return send_file(io.BytesIO(data), mimetype='image/png', as_attachment=True, download_name='no_bg.png')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate-api', methods=['POST'])
def generate_api():
    data = request.get_json()
    if not data or 'prompt' not in data:
        return jsonify({'error': 'No prompt'}), 400
    try:
        img = generate_image(data['prompt'], data.get('width', 512), data.get('height', 512))
        return send_file(io.BytesIO(img), mimetype='image/png')
    except ValueError:
        return jsonify({'error': 'Запрос содержит запрещённую тему.'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/chat-api', methods=['POST'])
def chat_api():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({'error': 'No message'}), 400
    try:
        return jsonify({'reply': generate_text(data['message'])})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/caption-api', methods=['POST'])
def caption_api():
    if 'image' not in request.files:
        return jsonify({'error': 'No image'}), 400
    try:
        return jsonify(caption_image(request.files['image'].read()))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/enhance-api', methods=['POST'])
def enhance_api():
    if 'image' not in request.files:
        return jsonify({'error': 'No image'}), 400
    try:
        data, _, _ = enhance_image(request.files['image'].read())
        return send_file(io.BytesIO(data), mimetype='image/png', as_attachment=True, download_name='enhanced.png')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# === Placeholder APIs ===
@app.route('/predict', methods=['POST'])
@app.route('/ocr-api', methods=['POST'])
@app.route('/restore-api', methods=['POST'])
def wip_api():
    return jsonify({'error': 'В разработке'}), 503

@app.route('/favicon.ico')
def favicon():
    return '', 204

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5001)
