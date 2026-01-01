import os
from dotenv import load_dotenv
from openai import OpenAI

# 1. Load the variables from the .env file
load_dotenv("api.env")

def analyze_resume(resume_text, job_desc):
    api_key = os.getenv("PERPLEXITY_API")
    if not api_key:
        raise ValueError("API Key not found! Ensure PERPLEXITY_API is set in your api.env file.")

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.perplexity.ai"
    )

    # Use a default message if job_desc is empty
    jd_content = job_desc if job_desc.strip() else "No specific job description provided. Provide a general professional critique."

    # Updated prompt with explicit BOLD instructions
    prompt = f"""
    Analyze the following resume against the job description.
    
    RESUME:
    {resume_text}
    
    JOB DESCRIPTION:
    {jd_content}
    
    Structure your response using these exact headers in BOLD:
    **KEYWORD GAP ANALYSIS**
    (List missing keywords here)

    **EXPERIENCE & SKILL GAPS**
    (List missing experience or certifications)

    **ACTIONABLE RECOMMENDATIONS**
    (List 3-4 specific ways to improve this resume)

    Keep it short, professional, and use bullet points.
    """
    
    response = client.chat.completions.create(
        model="sonar-pro",
        messages=[
            {
                "role": "system", 
                "content": "You are a professional ATS resume optimizer. Use Markdown for formatting. Bold all section headers."
            },
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content