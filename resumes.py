import json
from flask import (
    Blueprint, render_template, request, redirect,
    url_for, flash, abort, send_file
)
from flask_login import login_required, current_user
from database import db
from models import Resume
from utils.pdf import html_to_pdf
from io import BytesIO
from datetime import datetime

resumes_bp = Blueprint("resumes", __name__)

# -------------------------
# Dashboard
# -------------------------
@resumes_bp.get("/dashboard")
@login_required
def dashboard():
    resumes = Resume.query.filter_by(user_id=current_user.id).order_by(Resume.updated_at.desc()).all()
    return render_template("dashboard.html", resumes=resumes)

# -------------------------
# Create
# -------------------------
@resumes_bp.post("/resume/create")
@login_required
def create_resume():
    title = request.form.get("title", "My Resume").strip() or "My Resume"
    resume = Resume(user_id=current_user.id, title=title, data=_empty_resume_payload())
    db.session.add(resume)
    db.session.commit()
    flash("New resume created!", "success")
    return redirect(url_for("resumes.edit_resume", resume_id=resume.id))

# -------------------------
# Edit (Builder UI)
# -------------------------
@resumes_bp.get("/resume/<int:resume_id>/edit")
@login_required
def edit_resume(resume_id: int):
    resume = _get_owned_resume_or_404(resume_id)
    return render_template("resume_builder.html", resume=resume)

# -------------------------
# Save via API (autosave-ready)
# -------------------------
@resumes_bp.post("/api/resume/<int:resume_id>/save")
@login_required
def api_save_resume(resume_id: int):
    resume = _get_owned_resume_or_404(resume_id)
    try:
        payload = request.get_json(force=True)  # {basics, skills, experience, education, projects}
        if not isinstance(payload, dict):
            raise ValueError("Invalid data")
    except Exception as e:
        return {"ok": False, "error": f"Invalid JSON: {e}"}, 400

    resume.data = payload
    resume.updated_at = datetime.utcnow()
    db.session.commit()
    return {"ok": True}

# -------------------------
# Preview
# -------------------------
@resumes_bp.get("/resume/<int:resume_id>/preview")
@login_required
def preview_resume(resume_id: int):
    resume = _get_owned_resume_or_404(resume_id)
    return render_template("resume_preview.html", resume=resume)

# -------------------------
# Download PDF
# -------------------------
@resumes_bp.get("/resume/<int:resume_id>/download/pdf")
@login_required
def download_pdf(resume_id: int):
    resume = _get_owned_resume_or_404(resume_id)
    html = render_template("resume_preview.html", resume=resume, pdf_mode=True)
    pdf_bytes = html_to_pdf(html)
    return send_file(
        BytesIO(pdf_bytes),
        mimetype="application/pdf",
        as_attachment=True,
        download_name=f"{resume.title.replace(' ', '_').lower()}.pdf",
    )

# -------------------------
# Delete
# -------------------------
@resumes_bp.post("/resume/<int:resume_id>/delete")
@login_required
def delete_resume(resume_id: int):
    resume = _get_owned_resume_or_404(resume_id)
    db.session.delete(resume)
    db.session.commit()
    flash("Resume deleted successfully", "success")
    return redirect(url_for("resumes.dashboard"))

# -------------------------
# Duplicate
# -------------------------
@resumes_bp.post("/resume/<int:resume_id>/duplicate")
@login_required
def duplicate_resume(resume_id: int):
    resume = _get_owned_resume_or_404(resume_id)
    new_resume = Resume(
        user_id=current_user.id,
        title=f"{resume.title} (Copy)",
        data=resume.data,
        updated_at=datetime.utcnow()
    )
    db.session.add(new_resume)
    db.session.commit()
    flash("Resume duplicated!", "success")
    return redirect(url_for("resumes.edit_resume", resume_id=new_resume.id))

# -------------------------
# Helpers
# -------------------------
def _get_owned_resume_or_404(resume_id: int) -> Resume:
    resume = Resume.query.get_or_404(resume_id)
    if resume.user_id != current_user.id:
        abort(403)
    return resume

def _empty_resume_payload():
    return {
        "basics": {"full_name": "", "title": "", "email": "", "phone": "", "location": "", "summary": ""},
        "skills": [],       # list of strings
        "experience": [],   # list of {company, role, start, end, bullets: []}
        "education": [],    # list of {school, degree, start, end, details}
        "projects": [],     # list of {name, link, summary, bullets: []}
    }
