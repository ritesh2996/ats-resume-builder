import os
import docx2txt
import fitz  # PyMuPDF
from flask import Blueprint, request, render_template

ats_bp = Blueprint("ats", __name__)

def extract_text_from_file(file_path):
    """Extract text from PDF or DOCX"""
    if file_path.endswith(".pdf"):
        text = ""
        with fitz.open(file_path) as pdf:
            for page in pdf:
                text += page.get_text()
        return text
    elif file_path.endswith(".docx"):
        return docx2txt.process(file_path)
    return ""

@ats_bp.route("/api/check_ats", methods=["POST"])
def check_ats():
    file = request.files.get("resume_file")
    job_desc = request.form.get("job_description", "")

    if not file:
        return "No file uploaded", 400

    # Save uploaded file
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)
    file.save(file_path)

    # Extract text from resume
    resume_text = extract_text_from_file(file_path)

    # If job description provided → use its keywords
    if job_desc.strip():
        keywords = [word.strip(".,") for word in job_desc.split() if len(word) > 3]
    else:
        # Fallback skill list if no JD
        keywords = ["Python", "SQL", "Machine Learning", "Data Science",
                    "Communication", "Java", "C++", "Deep Learning", "AWS", "Tableau"]

    score = 0
    suggestions = []

    for kw in keywords:
        if kw.lower() in resume_text.lower():
            score += 100 // len(keywords)
        else:
            suggestions.append(f"Consider adding {kw}")

    score = min(score, 100)

    # Debug preview: first 300 chars of resume text
    preview_text = resume_text[:300] + ("..." if len(resume_text) > 300 else "")

    return render_template("ats_result.html",
                           score=score,
                           suggestions=suggestions,
                           preview=preview_text)

@ats_bp.route("/ats_result")
def ats_result():
    return render_template("ats_result.html", score=0, suggestions=[], preview="")
