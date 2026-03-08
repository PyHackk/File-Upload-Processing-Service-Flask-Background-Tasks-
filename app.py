from flask import Flask, request, jsonify, send_file
import os
import uuid
from werkzeug.utils import secure_filename
from PIL import Image
import threading
from datetime import datetime
import json

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['PROCESSED_FOLDER'] = 'processed'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Create directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)

# In-memory job tracking (use Redis in production)
jobs = {}

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'txt', 'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_file_async(job_id, filepath, file_type, options):
    """Background file processing"""
    try:
        jobs[job_id]['status'] = 'processing'
        
        if file_type in ['png', 'jpg', 'jpeg', 'gif']:
            # Image processing
            with Image.open(filepath) as img:
                # Resize if requested
                if options.get('resize'):
                    width, height = options['resize']
                    img = img.resize((width, height), Image.Resampling.LANCZOS)
                
                # Convert format if requested
                output_format = options.get('format', file_type).upper()
                if output_format == 'JPG':
                    output_format = 'JPEG'
                
                output_path = os.path.join(
                    app.config['PROCESSED_FOLDER'], 
                    f"{job_id}.{output_format.lower()}"
                )
                
                img.save(output_path, format=output_format, quality=90)
                
        elif file_type == 'txt':
            # Text processing - word count, line count
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            stats = {
                'word_count': len(content.split()),
                'line_count': len(content.splitlines()),
                'char_count': len(content),
                'char_count_no_spaces': len(content.replace(' ', ''))
            }
            
            output_path = os.path.join(
                app.config['PROCESSED_FOLDER'], 
                f"{job_id}_stats.json"
            )
            
            with open(output_path, 'w') as f:
                json.dump(stats, f, indent=2)
        
        jobs[job_id].update({
            'status': 'completed',
            'output_file': output_path,
            'completed_at': datetime.now().isoformat()
        })
        
    except Exception as e:
        jobs[job_id].update({
            'status': 'failed',
            'error': str(e),
            'completed_at': datetime.now().isoformat()
        })

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400
    
    # Generate unique job ID
    job_id = str(uuid.uuid4())
    filename = secure_filename(file.filename)
    file_ext = filename.rsplit('.', 1)[1].lower()
    
    # Save uploaded file
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{job_id}_{filename}")
    file.save(filepath)
    
    # Parse processing options
    options = {}
    if request.form.get('resize'):
        try:
            width, height = map(int, request.form.get('resize').split('x'))
            options['resize'] = (width, height)
        except:
            pass
    
    if request.form.get('format'):
        options['format'] = request.form.get('format')
    
    # Create job record
    jobs[job_id] = {
        'id': job_id,
        'filename': filename,
        'file_type': file_ext,
        'status': 'queued',
        'created_at': datetime.now().isoformat(),
        'options': options
    }
    
    # Start background processing
    thread = threading.Thread(
        target=process_file_async, 
        args=(job_id, filepath, file_ext, options)
    )
    thread.daemon = True
    thread.start()
    
    return jsonify({
        'job_id': job_id,
        'status': 'queued',
        'message': 'File uploaded and queued for processing'
    }), 202

@app.route('/status/<job_id>')
def get_job_status(job_id):
    job = jobs.get(job_id)
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    
    return jsonify(job)

@app.route('/download/<job_id>')
def download_file(job_id):
    job = jobs.get(job_id)
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    
    if job['status'] != 'completed':
        return jsonify({'error': 'Job not completed yet'}), 400
    
    return send_file(job['output_file'], as_attachment=True)

@app.route('/jobs')
def list_jobs():
    return jsonify(list(jobs.values()))

if __name__ == '__main__':
    app.run(debug=True)
        img.save(output_path, format=output_format, quality=90)
elif file_type == 'txt':
            # Text processing - word count, line count
            with open(filepath, 'r', encoding='utf-8') as f:

                content = f.read()

                

            stats = {

                'word_count': len(content.split()),

                'line_count': len(content.splitlines()),

                'char_count': len(content)

            }

            

            output_path = os.path.join(

                app.config['PROCESSED_FOLDER'], 

                f"{job_id}_stats.json"

            )

            

            with open(output_path, 'w') as f:

                json.dump(stats, f, indent=2)

        

        jobs[job_id]['status'] = 'completed'

        jobs[job_id]['output_file'] = output_path

        jobs[job_id]['completed_at'] = datetime.now().isoformat()

        

    except Exception as e:

        jobs[job_id]['status'] = 'failed'

        jobs[job_id]['error'] = str(e)

@app.route('/upload', methods=['POST'])

def upload_file():

    if 'file' not in request.files:

        return jsonify({'error': 'No file provided'}), 400

    

    file = request.files['file']

    if file.filename == '':

        return jsonify({'error': 'No file selected'}), 400

    

    if not allowed_file(file.filename):

        return jsonify({'error': 'File type not allowed'}), 400

    

    # Generate unique job ID

    job_id = str(uuid.uuid4())

    filename = secure_filename(file.filename)

    file_ext = filename.rsplit('.', 1)[1].lower()

    

    # Save file

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{job_id}_{filename}")

    file.save(filepath)

    

    # Parse processing options

    options = {}

    if request.form.get('resize'):

        try:

            width, height = map(int, request.form['resize'].split('x'))

            options['resize'] = (width, height)

        except:

            pass

    

    if request.form.get('format'):

        options['format'] = request.form['format']

    

    # Create job record

    jobs[job_id] = {

        'id': job_id,

        'filename': filename,

        'file_type': file_ext,

        'status': 'queued',

        'created_at': datetime.now().isoformat(),

        'options': options

    }

    

    # Start background processing

    thread = threading.Thread(

        target=process_file_async,

        args=(job_id, filepath, file_ext, options)

    )

    thread.start()

    

    return jsonify({

        'job_id': job_id,

        'status': 'queued',

        'message': 'File uploaded and processing started'

    }), 202

@app.route('/status/<job_id>')

def get_job_status(job_id):

    if job_id not in jobs:

        return jsonify({'error': 'Job not found'}), 404

    

    return jsonify(jobs[job_id])

@app.route('/download/<job_id>')

def download_file(job_id):

    if job_id not in jobs:

        return jsonify({'error': 'Job not found'}), 404

    

    job = jobs[job_id]

    if job['status'] != 'completed':

        return jsonify({'error': 'Job not completed'}), 400

    

    return send_file(job['output_file'], as_attachment=True)

@app.route('/jobs')

def list_jobs():

    return jsonify(list(jobs.values()))

if __name__ == '__main__':

    app.run(debug=True)
