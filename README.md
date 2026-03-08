# File Upload & Processing Service

A robust file processing service that handles image resizing, format conversion, and text analysis with background job processing.

## 🚀 Features

- **Multi-format Support**: Images (PNG, JPG, GIF), Text files, PDFs, CSV
- **Image Processing**: Resize, format conversion, quality optimization  
- **Text Analysis**: Word count, line count, character statistics
- **Background Processing**: Non-blocking file processing with job tracking
- **RESTful API**: Clean endpoints for upload, status checking, and download
- **Job Management**: Track processing status and history

## 📋 Requirements

- Python 3.8+
- Flask 3.0+
- Pillow (PIL) for image processing
- 16MB max file size (configurable)

## ⚡ Quick Start
Clone the repository

git clone https://github.com/yourusername/file-processor.git

cd file-processor

Install dependencies

pip install -r requirements.txt

Create upload directories

mkdir uploads processed

Run the application

python app.py

Server runs on `http://localhost:5000`

## 📚 API Documentation

### Upload File
Upload and queue file for processing.
