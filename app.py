import os
import io
import base64
from flask import Flask, render_template, request, jsonify
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch
from dotenv import load_dotenv

# Load environment variables
load_dotenv('config.env')

app = Flask(__name__)

# Configuration from environment variables
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 209715200))  # Default 200MB
FLASK_HOST = os.getenv('FLASK_HOST', '0.0.0.0')
FLASK_PORT = int(os.getenv('FLASK_PORT', 8001))
FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
HUGGINGFACE_MODEL = os.getenv('HUGGINGFACE_MODEL', 'Salesforce/blip-image-captioning-base')
HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY', '')
MODEL_CACHE_DIR = os.getenv('MODEL_CACHE_DIR', '.cache/huggingface')
ALLOWED_EXTENSIONS = os.getenv('ALLOWED_EXTENSIONS', 'jpg,jpeg,png').split(',')

# Initialize the Hugging Face model
processor = None
model = None

def load_model():
    """Load the BLIP model for image captioning"""
    global processor, model
    try:
        # Set cache directory
        os.environ['TRANSFORMERS_CACHE'] = MODEL_CACHE_DIR
        
        # Set Hugging Face token if provided
        if HUGGINGFACE_API_KEY and HUGGINGFACE_API_KEY != 'your_huggingface_api_key_here':
            os.environ['HF_TOKEN'] = HUGGINGFACE_API_KEY
            os.environ['HUGGINGFACE_HUB_TOKEN'] = HUGGINGFACE_API_KEY  # Backup for compatibility
            print("✅ Hugging Face API key configured successfully")
        
        print(f"🤖 Loading model: {HUGGINGFACE_MODEL}")
        processor = BlipProcessor.from_pretrained(HUGGINGFACE_MODEL)
        model = BlipForConditionalGeneration.from_pretrained(HUGGINGFACE_MODEL)
        print(f"✅ Model '{HUGGINGFACE_MODEL}' loaded successfully!")
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        if "401" in str(e) or "unauthorized" in str(e).lower():
            print("🔑 This might be due to an invalid API key. Check your HUGGINGFACE_API_KEY in config.env")
        elif "gated" in str(e).lower() or "private" in str(e).lower():
            print("🔒 This model requires authentication. Make sure your API key has access to this model.")
        else:
            print("💡 Try checking your internet connection or model name.")

def generate_caption(image):
    """Generate caption for the uploaded image"""
    try:
        if processor is None or model is None:
            return "Model not loaded. Please try again later."
        
        # Process the image
        inputs = processor(image, return_tensors="pt")
        
        # Generate caption
        with torch.no_grad():
            outputs = model.generate(**inputs, max_length=50, num_beams=5)
        
        # Decode the generated text
        caption = processor.decode(outputs[0], skip_special_tokens=True)
        return caption
    
    except Exception as e:
        return f"Error generating caption: {str(e)}"

@app.route('/')
def index():
    """Main page with upload form"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    """Handle image upload and generate caption"""
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Check file type using environment variable
        file_ext = file.filename.lower().split('.')[-1] if '.' in file.filename else ''
        if file_ext not in ALLOWED_EXTENSIONS:
            return jsonify({'error': f'Invalid file type. Please upload {", ".join(ALLOWED_EXTENSIONS).upper()} images.'}), 400
        
        # Read and process the image
        image_data = file.read()
        image = Image.open(io.BytesIO(image_data)).convert('RGB')
        
        # Convert image to base64 for display
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        image_base64 = base64.b64encode(buffered.getvalue()).decode()
        
        # Generate caption
        caption = generate_caption(image)
        
        return jsonify({
            'success': True,
            'image': f"data:image/jpeg;base64,{image_base64}",
            'caption': caption
        })
    
    except Exception as e:
        return jsonify({'error': f'Error processing image: {str(e)}'}), 500

if __name__ == '__main__':
    print("Loading AI model...")
    load_model()
    print(f"Starting Flask application on {FLASK_HOST}:{FLASK_PORT}")
    print(f"Debug mode: {FLASK_DEBUG}")
    app.run(debug=FLASK_DEBUG, host=FLASK_HOST, port=FLASK_PORT)
