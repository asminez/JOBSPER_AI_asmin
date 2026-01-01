# Quick Start Guide

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python app.py
```

### 3. Access the Application
Open your browser and navigate to: http://localhost:5000

### 4. Usage Steps
1. Click the upload area or drag and drop your resume file (supports PDF, DOC, DOCX, TXT)
2. Click the "Generate Template" button
3. Review the parsing results
4. Download the generated template resume

## Notes

- Ensure `uploads/` and `output/` folders have write permissions
- File size limit: 16MB
- Supported formats: PDF, DOC, DOCX, TXT
- Make sure to add api key in your a new env file, make a file called, api.env and add PERPLEXITY_API = "our api key", make sure you put env file in git ignore so we dont reveal our api key
- Also install openai , pip install openai
