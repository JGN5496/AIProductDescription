# AI Product Description Generator

A Flask web application that uses Hugging Face's BLIP model to generate descriptive text from uploaded images.

## Features

- 🖼️ Image upload with drag & drop functionality
- 📸 Real-time image preview
- 🤖 AI-powered image description using Hugging Face BLIP model
- 📱 Responsive, modern UI design
- ⚡ Fast processing with local model inference

## Setup Instructions

### 1. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Configure Environment

Copy the example configuration file and customize it:
```bash
cp config.env .env  # Create your own environment file
```

Edit the `.env` file to customize settings:
- `FLASK_PORT`: Port number (default: 5000)
- `FLASK_HOST`: Host address (default: 0.0.0.0)
- `FLASK_DEBUG`: Debug mode (default: True)
- `HUGGINGFACE_API_KEY`: Your Hugging Face API key (optional)
- `HUGGINGFACE_MODEL`: Model to use (default: Salesforce/blip-image-captioning-base)
- `MAX_CONTENT_LENGTH`: Max file size in bytes (default: 200MB)
- `ALLOWED_EXTENSIONS`: Supported file types (default: jpg,jpeg,png)

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

**Option A: Using the startup script (recommended)**
```bash
./run_app.sh
```

**Option B: Manual start**
```bash
source venv/bin/activate  # If not already activated
python app.py
```

The application will be available at `http://localhost:5000` (or the port specified in your `.env` file)

### 5. Using the Application

1. Open your web browser and navigate to `http://localhost:5000`
2. Upload an image by either:
   - Clicking "Browse files" and selecting an image
   - Dragging and dropping an image file onto the upload area
3. Wait for the AI model to process the image
4. View the generated description below the image preview

## Supported File Formats

- JPG/JPEG
- PNG
- Maximum file size: 200MB

## Model Information

This application uses the Salesforce BLIP (Bootstrapping Language-Image Pre-training) model for image captioning:
- Model: `Salesforce/blip-image-captioning-base`
- Framework: Hugging Face Transformers
- Inference: Local CPU/GPU processing

## Environment Configuration

The application uses environment variables for configuration. Available settings:

| Variable | Description | Default Value |
|----------|-------------|---------------|
| `FLASK_PORT` | Port number for the Flask app | `5000` |
| `FLASK_HOST` | Host address | `0.0.0.0` |
| `FLASK_DEBUG` | Enable debug mode | `True` |
| `HUGGINGFACE_MODEL` | Model to use for image captioning | `Salesforce/blip-image-captioning-base` |
| `HUGGINGFACE_API_KEY` | Your Hugging Face API key (optional) | `your_huggingface_api_key_here` |
| `MAX_CONTENT_LENGTH` | Maximum file upload size in bytes | `209715200` (200MB) |
| `ALLOWED_EXTENSIONS` | Comma-separated list of allowed file extensions | `jpg,jpeg,png` |
| `MODEL_CACHE_DIR` | Directory for caching downloaded models | `.cache/huggingface` |

## Requirements

- Python 3.8+
- Flask 3.0.0
- PyTorch 2.1.0+
- Transformers 4.36.0
- Pillow 10.0.0+
- python-dotenv 1.0.0+

## Project Structure

```
AIProductDescription/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── config.env            # Environment configuration template
├── run_app.sh            # Startup script
├── .gitignore            # Git ignore file
├── README.md             # This file
├── venv/                 # Virtual environment (after setup)
├── templates/
│   └── index.html        # Main page template
└── static/
    ├── css/
    │   └── style.css     # Application styles
    └── js/
        └── script.js     # Frontend JavaScript
```

## Notes

- The model will download automatically on first run (~1GB)
- Processing time depends on image size and hardware capabilities
- For best performance, use images under 10MB
