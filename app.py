from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
import os
import json
from werkzeug.utils import secure_filename

# Import your custom modules
from resume_parser import ResumeParser
from resume_generator import ResumeGenerator
from llm import analyze_resume  # Assuming your LLM code is in llm_service.py

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/upload', methods=['POST'])
def upload_file():
    # 1. Check for file
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    # 2. Get Job Description from the frontend (from your new textarea)
    job_desp = request.form.get('job_description', '')
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # 3. Parse resume to get structured data
            parser = ResumeParser()
            resume_data = parser.parse(filepath)
            
            # 4. Call your LLM function for Analysis
            # We convert resume_data (dict) to a string so Perplexity can read it
            analysis_text = analyze_resume(json.dumps(resume_data), job_desp)
            
            # 5. Generate the document template
            generator = ResumeGenerator()
            output_path = generator.generate(resume_data, filename)
            
            # 6. Return EVERYTHING back to the HTML
            return jsonify({
                'success': True,
                'resume_data': resume_data,
                'llm_analysis': analysis_text,  # This displays in your <pre> box
                'output_file': os.path.basename(output_path)
            }), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/api/download/<filename>')
def download_file(filename):
    filepath = os.path.join(app.config['OUTPUT_FOLDER'], filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)