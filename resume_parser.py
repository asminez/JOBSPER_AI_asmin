import os
import re
from datetime import datetime
from docx import Document
import PyPDF2
import pdfplumber

class ResumeParser:
    def __init__(self):
        self.text = ""
    
    def parse(self, filepath):
        """Parse resume file and extract structured information"""
        file_ext = os.path.splitext(filepath)[1].lower()
        
        if file_ext == '.pdf':
            self.text = self._extract_from_pdf(filepath)
        elif file_ext in ['.doc', '.docx']:
            self.text = self._extract_from_docx(filepath)
        elif file_ext == '.txt':
            with open(filepath, 'r', encoding='utf-8') as f:
                self.text = f.read()
        else:
            raise ValueError(f"Unsupported file format: {file_ext}")
        
        return self._extract_resume_data()
    
    def _extract_from_pdf(self, filepath):
        """Extract text from PDF"""
        text = ""
        try:
            with pdfplumber.open(filepath) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() + "\n"
        except:
            # Fallback method
            with open(filepath, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
        return text
    
    def _extract_from_docx(self, filepath):
        """Extract text from Word document"""
        doc = Document(filepath)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text
    
    def _extract_resume_data(self):
        """Extract structured resume data from text"""
        lines = [line.strip() for line in self.text.split('\n') if line.strip()]
        
        resume_data = {
            'personal_info': self._extract_personal_info(),
            'education': self._extract_education(),
            'work_experience': self._extract_work_experience(),
            'skills': self._extract_skills(),
            'projects': self._extract_projects(),
            'certifications': self._extract_certifications(),
            'languages': self._extract_languages(),
            'awards': self._extract_awards(),
            'summary': self._extract_summary()
        }
        
        return resume_data
    
    def _extract_personal_info(self):
        """Extract personal information"""
        info = {
            'name': '',
            'email': '',
            'phone': '',
            'address': '',
            'linkedin': '',
            'github': '',
            'website': ''
        }
        
        # Extract email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, self.text)
        if emails:
            info['email'] = emails[0]
        
        # Extract phone (supports English and Chinese formats)
        phone_patterns = [
            r'\+?[\d\s\-\(\)]{10,}',  # General format
            r'1?\s*\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',  # English format
            r'1[3-9]\d{9}',  # Chinese mobile: 138xxxxxxxx
            r'\d{3}[-.\s]?\d{4}[-.\s]?\d{4}',  # Chinese mobile with separators
            r'0\d{2,3}[-.\s]?\d{7,8}',  # Chinese landline
        ]
        for pattern in phone_patterns:
            phones = re.findall(pattern, self.text[:500])
            if phones:
                info['phone'] = phones[0].strip()
                break
        
        # Extract LinkedIn
        linkedin_pattern = r'linkedin\.com/in/[\w\-]+'
        linkedin = re.search(linkedin_pattern, self.text, re.IGNORECASE)
        if linkedin:
            info['linkedin'] = 'https://' + linkedin.group()
        
        # Extract GitHub
        github_pattern = r'github\.com/[\w\-]+'
        github = re.search(github_pattern, self.text, re.IGNORECASE)
        if github:
            info['github'] = 'https://' + github.group()
        
        # Extract website
        website_pattern = r'https?://(?!linkedin|github)[\w\.\-]+\.[a-z]{2,}'
        website = re.search(website_pattern, self.text, re.IGNORECASE)
        if website:
            info['website'] = website.group()
        
        # Extract name (usually at the beginning of the document)
        first_lines = [line for line in self.text.split('\n')[:10] if line.strip()]
        if first_lines:
            # Assume first or second line is the name
            potential_name = first_lines[0].strip()
            if len(potential_name.split()) <= 4 and not '@' in potential_name:
                info['name'] = potential_name
        
        return info
    
    def _extract_education(self):
        """Extract education background"""
        education = []
        # Support English and Chinese keywords
        education_keywords = [
            'education', 'university', 'college', 'degree', 'bachelor', 'master', 'phd', 'diploma', 'school',
            '教育', '学历', '教育背景', '教育经历', '大学', '学院', '学校', '毕业', '学位', '本科', '硕士', '博士', '学士'
        ]
        
        lines = self.text.split('\n')
        current_edu = None
        
        for i, line in enumerate(lines):
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in education_keywords):
                if current_edu:
                    education.append(current_edu)
                current_edu = {
                    'institution': line.strip(),
                    'degree': '',
                    'major': '',
                    'period': '',
                    'gpa': '',
                    'description': ''
                }
            elif current_edu:
                # Extract degree (supports English and Chinese)
                degree_patterns = [
                    'bachelor', 'master', 'phd', 'doctor', 'associate', 'diploma',
                    '本科', '学士', '硕士', '博士', '专科', '研究生', '博士研究生', '硕士研究生'
                ]
                for degree in degree_patterns:
                    if degree in line_lower:
                        current_edu['degree'] = line.strip()
                        break
                
                # Extract time period
                year_pattern = r'\d{4}'
                years = re.findall(year_pattern, line)
                if years:
                    current_edu['period'] = line.strip()
        
        if current_edu:
            education.append(current_edu)
        
        return education[:5]  # Return maximum 5 entries
    
    def _extract_work_experience(self):
        """Extract work experience"""
        experience = []
        # Support English and Chinese keywords
        work_keywords = [
            'experience', 'employment', 'work', 'position', 'job', 'career', 'company',
            '工作', '工作经历', '工作经验', '工作履历', '职业经历', '任职', '就职', '公司', '职位', '岗位'
        ]
        
        lines = self.text.split('\n')
        current_exp = None
        
        for i, line in enumerate(lines):
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in work_keywords):
                if current_exp:
                    experience.append(current_exp)
                current_exp = {
                    'company': '',
                    'position': '',
                    'period': '',
                    'location': '',
                    'description': []
                }
                # Try to extract company name and position (supports English and Chinese formats)
                # English format: Position at Company or Position in Company
                if 'at' in line_lower or 'in' in line_lower:
                    parts = re.split(r'\s+at\s+|\s+in\s+', line, flags=re.IGNORECASE)
                    if len(parts) >= 2:
                        current_exp['position'] = parts[0].strip()
                        current_exp['company'] = parts[1].strip()
                # Chinese format: Company | Position or Position | Company
                elif '|' in line or '｜' in line:
                    parts = re.split(r'\s*\|\s*|｜', line)
                    if len(parts) >= 2:
                        # Determine which is company name and which is position (usually position comes first)
                        current_exp['position'] = parts[0].strip()
                        current_exp['company'] = parts[1].strip()
                else:
                    current_exp['company'] = line.strip()
            elif current_exp:
                # Extract time period
                year_pattern = r'\d{4}'
                years = re.findall(year_pattern, line)
                if years:
                    current_exp['period'] = line.strip()
                elif line.strip() and not line.strip().startswith('-'):
                    if len(current_exp['description']) < 5:
                        current_exp['description'].append(line.strip())
        
        if current_exp:
            experience.append(current_exp)
        
        return experience[:10]  # Return maximum 10 entries
    
    def _extract_skills(self):
        """Extract skills"""
        skills = []
        # Support English and Chinese keywords
        skill_keywords = [
            'skill', 'technical', 'proficiency', 'expertise', 'competence',
            '技能', '专业技能', '技术技能', '能力', '专长', '技术', '掌握', '熟悉', '精通'
        ]
        
        lines = self.text.split('\n')
        in_skills_section = False
        
        for line in lines:
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in skill_keywords):
                in_skills_section = True
                continue
            
            if in_skills_section:
                # Extract skill items (usually separated by comma, semicolon, or newline)
                if line.strip():
                    skill_items = re.split(r'[,;|•\-\n]', line)
                    for item in skill_items:
                        item = item.strip()
                        if item and len(item) > 1:
                            skills.append(item)
                    if len(skills) > 20:  # Limit number of skills
                        break
        
        # If skills section not found, try to extract common technical terms from entire document
        if not skills:
            common_skills = ['python', 'java', 'javascript', 'react', 'vue', 'angular', 
                           'node', 'sql', 'mongodb', 'docker', 'kubernetes', 'aws', 
                           'git', 'linux', 'html', 'css', 'typescript', 'spring', 
                           'django', 'flask', 'express', 'mysql', 'postgresql']
            text_lower = self.text.lower()
            for skill in common_skills:
                if skill in text_lower:
                    skills.append(skill.capitalize())
        
        return list(set(skills))[:30]  # Remove duplicates and limit quantity
    
    def _extract_projects(self):
        """Extract project experience"""
        projects = []
        # Support English and Chinese keywords
        project_keywords = [
            'project', 'portfolio', 'development',
            '项目', '项目经验', '项目经历', '作品', '开发', '项目作品'
        ]
        
        lines = self.text.split('\n')
        current_project = None
        
        for line in lines:
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in project_keywords):
                if current_project:
                    projects.append(current_project)
                current_project = {
                    'name': line.strip(),
                    'description': '',
                    'technologies': [],
                    'period': ''
                }
            elif current_project:
                if line.strip():
                    if not current_project['description']:
                        current_project['description'] = line.strip()
                    else:
                        current_project['description'] += ' ' + line.strip()
        
        if current_project:
            projects.append(current_project)
        
        return projects[:10]
    
    def _extract_certifications(self):
        """Extract certifications"""
        certifications = []
        # Support English and Chinese keywords
        cert_keywords = [
            'certification', 'certificate', 'certified', 'license',
            '证书', '认证', '资格证', '资质', '执照', '资格认证'
        ]
        
        lines = self.text.split('\n')
        for line in lines:
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in cert_keywords):
                cert = {
                    'name': line.strip(),
                    'issuer': '',
                    'date': ''
                }
                # Extract date
                year_pattern = r'\d{4}'
                years = re.findall(year_pattern, line)
                if years:
                    cert['date'] = years[0]
                certifications.append(cert)
        
        return certifications[:10]
    
    def _extract_languages(self):
        """Extract language skills"""
        languages = []
        # Support English and Chinese keywords
        language_keywords = [
            'language', 'languages', 'english', 'chinese', 'spanish', 'french', 'german',
            '语言', '语言能力', '外语', '英语', '中文', '普通话', '粤语'
        ]
        
        lines = self.text.split('\n')
        in_lang_section = False
        
        for line in lines:
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in language_keywords):
                in_lang_section = True
                continue
            
            if in_lang_section:
                if line.strip():
                    lang_items = re.split(r'[,;|•\-\n]', line)
                    for item in lang_items:
                        item = item.strip()
                        if item:
                            languages.append(item)
        
        return languages[:10]
    
    def _extract_awards(self):
        """Extract awards and honors"""
        awards = []
        # Support English and Chinese keywords
        award_keywords = [
            'award', 'honor', 'achievement', 'recognition', 'prize',
            '奖项', '荣誉', '奖励', '获奖', '成就', '表彰', '嘉奖'
        ]
        
        lines = self.text.split('\n')
        for line in lines:
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in award_keywords):
                award = {
                    'name': line.strip(),
                    'date': ''
                }
                year_pattern = r'\d{4}'
                years = re.findall(year_pattern, line)
                if years:
                    award['date'] = years[0]
                awards.append(award)
        
        return awards[:10]
    
    def _extract_summary(self):
        """Extract personal summary/objective"""
        # Support English and Chinese keywords
        summary_keywords = [
            'summary', 'objective', 'profile', 'about', 'introduction',
            '简介', '个人简介', '自我评价', '个人介绍', '概述', '个人概述', '职业目标'
        ]
        lines = self.text.split('\n')
        
        summary_lines = []
        in_summary = False
        
        for line in lines:
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in summary_keywords):
                in_summary = True
                continue
            
            if in_summary:
                if line.strip():
                    summary_lines.append(line.strip())
                if len(summary_lines) >= 5:  # Limit summary length
                    break
        
        return ' '.join(summary_lines)

