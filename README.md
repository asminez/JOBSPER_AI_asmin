# Resume Template Generator

A web application that automatically analyzes uploaded resumes and generates professional, standardized resume templates. Users can upload their resumes in various formats (PDF, DOC, DOCX, TXT), and the system will extract structured information and create a well-formatted template.

## Features

- **Multi-format Support**: Accepts PDF, Word documents (DOC, DOCX), and plain text files
- **Intelligent Parsing**: Automatically extracts key resume sections including:
  - Personal information (name, contact details, social profiles)
  - Professional summary
  - Work experience
  - Education background
  - Skills and technical competencies
  - Projects and portfolio items
  - Certifications
  - Languages
  - Awards and honors
- **Template Generation**: Creates professional Word document templates with consistent formatting
- **Web Interface**: User-friendly drag-and-drop upload interface
- **RESTful API**: Backend API for easy integration with other systems

## Technology Stack

### Backend
- **Flask**: Python web framework for API endpoints
- **python-docx**: Word document generation
- **PyPDF2 & pdfplumber**: PDF text extraction
- **python-dateutil**: Date parsing utilities

### Frontend
- **HTML5/CSS3**: Modern, responsive user interface
- **Vanilla JavaScript**: Client-side file handling and API communication

## Project Structure

```
Jobsper_AI/
├── app.py                 # Main Flask application
├── resume_parser.py       # Resume parsing and extraction logic
├── resume_generator.py    # Template generation engine
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Web interface
├── uploads/              # Temporary storage for uploaded files
└── output/               # Generated resume templates
```

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone or navigate to the project directory**
   ```bash
   cd Jobsper_AI
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the web interface**
   Open your browser and navigate to: `http://localhost:5000`

## Usage

### Web Interface

1. **Upload Resume**
   - Click the upload area or drag and drop your resume file
   - Supported formats: PDF, DOC, DOCX, TXT
   - Maximum file size: 16MB

2. **Generate Template**
   - Click the "Generate Template" button
   - Wait for the system to process your resume

3. **Review & Download**
   - View the extracted resume data in JSON format
   - Download the generated Word document template

### API Endpoints

#### Upload and Process Resume
```
POST /api/upload
Content-Type: multipart/form-data

Request:
- file: Resume file (PDF, DOC, DOCX, or TXT)

Response:
{
  "success": true,
  "resume_data": {
    "personal_info": {...},
    "education": [...],
    "work_experience": [...],
    "skills": [...],
    ...
  },
  "output_file": "resume_template_20240101_120000.docx"
}
```

#### Download Generated Template
```
GET /api/download/<filename>

Response: Word document file download
```

## Resume Data Structure

The parser extracts the following information:

### Personal Information
- Name
- Email address
- Phone number
- Physical address
- LinkedIn profile
- GitHub profile
- Personal website

### Professional Summary
- Career objective or professional summary text

### Work Experience
- Company name
- Job title/position
- Employment period
- Location
- Job description and responsibilities

### Education
- Institution name
- Degree type
- Major/field of study
- Graduation period
- GPA (if available)

### Skills
- Technical skills
- Programming languages
- Tools and technologies
- Soft skills

### Projects
- Project name
- Description
- Technologies used
- Time period

### Certifications
- Certification name
- Issuing organization
- Date obtained

### Languages
- Language proficiency levels

### Awards & Honors
- Award name
- Date received

## Configuration

### File Upload Settings
Edit `app.py` to modify:
- `MAX_CONTENT_LENGTH`: Maximum file size (default: 16MB)
- `ALLOWED_EXTENSIONS`: Supported file types
- `UPLOAD_FOLDER`: Directory for uploaded files
- `OUTPUT_FOLDER`: Directory for generated templates

### Parsing Customization
Modify `resume_parser.py` to:
- Adjust extraction patterns
- Add custom field recognition
- Improve accuracy for specific resume formats

### Template Styling
Edit `resume_generator.py` to customize:
- Font styles and sizes
- Color schemes
- Section ordering
- Layout preferences

## Limitations & Future Enhancements

### Current Limitations
- Parsing accuracy depends on resume format consistency
- Complex layouts may require manual review
- Image-based PDFs may not extract text properly

### Planned Enhancements
- [ ] Support for more file formats (RTF, ODT)
- [ ] Multiple template styles/themes
- [ ] PDF output option
- [ ] Resume validation and completeness scoring
- [ ] ATS (Applicant Tracking System) optimization suggestions
- [x] Multi-language support (English & Chinese)
- [ ] Batch processing capability
- [ ] User authentication and resume storage
- [ ] Integration with job boards and ATS systems

## Development Notes for Web Page Implementation

### Frontend Integration Points

1. **File Upload Component**
   - The upload area uses standard HTML5 file input
   - Drag-and-drop functionality is implemented with JavaScript
   - File validation happens client-side before upload

2. **API Communication**
   - Uses Fetch API for HTTP requests
   - Handles file uploads via FormData
   - Error handling with user-friendly messages

3. **UI/UX Considerations**
   - Responsive design works on mobile and desktop
   - Loading states with progress indicators
   - Clear visual feedback for all actions

### Backend Integration Points

1. **Flask Routes**
   - `/`: Serves the main HTML interface
   - `/api/upload`: Handles file upload and processing
   - `/api/download/<filename>`: Serves generated files

2. **Error Handling**
   - Returns JSON error responses with descriptive messages
   - Handles file type and size validation
   - Graceful error recovery

3. **File Management**
   - Uploaded files stored temporarily in `uploads/` folder
   - Generated templates saved in `output/` folder
   - Consider implementing cleanup for old files in production

### Production Deployment Considerations

1. **Security**
   - Implement file type validation on server-side
   - Add file size limits
   - Sanitize filenames
   - Consider virus scanning for uploaded files
   - Add rate limiting to prevent abuse

2. **Performance**
   - Implement file caching
   - Add background job processing for large files
   - Consider using Celery for async processing
   - Optimize PDF parsing for large documents

3. **Scalability**
   - Use cloud storage (S3, Azure Blob) for file storage
   - Implement database for resume metadata
   - Add user session management
   - Consider microservices architecture for scaling

4. **Monitoring**
   - Add logging for debugging
   - Implement error tracking (Sentry, etc.)
   - Monitor API response times
   - Track usage metrics

## Troubleshooting

### Common Issues

1. **File upload fails**
   - Check file size (must be < 16MB)
   - Verify file format is supported
   - Ensure uploads/ directory has write permissions

2. **Parsing returns empty data**
   - Resume may have complex formatting
   - Try converting to plain text first
   - Check if PDF is image-based (OCR may be needed)

3. **Generated template looks incorrect**
   - Review extracted data in JSON output
   - Manually adjust parser patterns if needed
   - Check Word document formatting settings

## License

This project is provided as-is for demonstration purposes.

## Contributing

For web page development, please refer to the integration points mentioned above. The backend API is ready for frontend integration, and the current HTML interface can serve as a reference implementation.

## Contact & Support

For questions or issues related to web page development, please refer to the code comments in `app.py`, `resume_parser.py`, and `resume_generator.py` for detailed implementation notes.

