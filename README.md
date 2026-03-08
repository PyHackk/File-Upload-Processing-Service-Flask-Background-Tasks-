# File Upload & Processing Service

A Flask-based service for uploading and processing files with background task support. Handles image resizing, format conversion, and text analysis.

## 🚀 Features

- **Multi-format Support**: Images (PNG, JPG, GIF), Text files, PDFs

- **Image Processing**: Resize, format conversion, quality optimization

- **Text Analysis**: Word count, line count, character statistics

- **Background Processing**: Non-blocking file processing with job tracking

- **Progress Monitoring**: Real-time job status updates

- **Secure Uploads**: File validation and secure filename handling

## 📋 Quick Start

Clone repository

git clone https://github.com/yourusername/file-processor.git

cd file-processor

Install dependencies

pip install -r requirements.txt

Create directories

mkdir uploads processed

Run application

python app.py
code

## 🔧 API Endpoints

### Upload File

POST /upload

Content-Type: multipart/form-data

file: [binary file]

resize: "800x600" (optional, for images)

format: "png" (optional, for images)
code

**Response:**

{

"job_id": "123e4567-e89b-12d3-a456-426614174000",

"status": "queued",

"message": "File uploaded and processing started"

}
code

### Check Job Status

GET /status/{job_id}
code

**Response:**

{

"id": "123e4567-e89b-12d3-a456-426614174000",

"filename": "image.jpg",

"file_type": "jpg",

"status": "completed",

"created_at": "2024-01-15T10:30:00",

"completed_at": "2024-01-15T10:30:05",

"options": {

"resize": [800, 600],

"format": "png"

}

}
code

### Download Processed File

GET /download/{job_id}
code

### List All Jobs

GET /jobs
code

## 📝 Usage Examples

### Resize Image

curl -X POST -F "file=@image.jpg" -F "resize=800x600" http://localhost:5000/upload
code

### Convert Image Format

curl -X POST -F "file=@image.jpg" -F "format=png" http://localhost:5000/upload
code

### Process Text File

curl -X POST -F "file=@document.txt" http://localhost:5000/upload
code

### Check Processing Status

curl http://localhost:5000/status/123e4567-e89b-12d3-a456-426614174000
code

## 🏗️ Architecture

- **Flask**: Web framework and API endpoints

- **PIL/Pillow**: Image processing and manipulation

- **Threading**: Background task processing

- **Werkzeug**: Secure file handling utilities

## 🔒 Security Features

- File type validation

- Secure filename sanitization

- File size limits (16MB default)

- Input validation for processing options

## 📊 Supported Operations

### Images

- **Resize**: Custom dimensions with aspect ratio preservation

- **Format Conversion**: PNG, JPG, GIF interconversion

- **Quality Optimization**: Automatic compression

### Text Files

- **Word Count**: Total words in document

- **Line Count**: Number of lines

- **Character Analysis**: Total characters including/excluding spaces

## 🚀 Production Deployment

For production use:

1. **Replace in-memory storage** with Redis/database

2. **Add authentication** and rate limiting

3. **Use Celery** for robust background processing

4. **Implement file cleanup** for processed files

5. **Add logging** and monitoring

6. **Configure reverse proxy** (Nginx)

## 🛠️ Environment Variables

Create `.env` file:

FLASK_ENV=production

MAX_FILE_SIZE=16777216
