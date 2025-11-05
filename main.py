from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
from flask_session import Session
import os
from dotenv import load_dotenv
from servicio_language import analizar_sentimiento
from servicio_translator import traducir_texto
from servicio_vision import describir_imagen

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-123')
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False

# Inicializar extensiones
CORS(app)
Session(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze-text', methods=['POST'])
def analyze_text():
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({'success': False, 'error': 'No se proporcionó texto'}), 400
        
        # Análisis de sentimiento
        sentiment = analizar_sentimiento(text)
        
        # Traducción al inglés
        translation = traducir_texto(text, "en")
        
        return jsonify({
            'success': True,
            'sentiment': sentiment,
            'translation': translation
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/analyze-image', methods=['POST'])
def analyze_image():
    try:
        if 'image' not in request.files:
            return jsonify({'success': False, 'error': 'No se proporcionó ninguna imagen'}), 400
        
        image_file = request.files['image']
        temp_path = 'temp_image.jpg'
        image_file.save(temp_path)
        
        # Análisis de imagen
        description = describir_imagen(temp_path)
        
        # Eliminar archivo temporal
        if os.path.exists(temp_path):
            os.remove(temp_path)
        
        return jsonify({
            'success': True,
            'description': description
        })
    except Exception as e:
        if os.path.exists('temp_image.jpg'):
            os.remove('temp_image.jpg')
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # Crear carpeta para sesiones si no existe
    if not os.path.exists('sessions'):
        os.makedirs('sessions')
    
    app.run(debug=True, port=5000)
