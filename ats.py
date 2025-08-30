from flask import Blueprint, request, jsonify, render_template

ats_bp = Blueprint("ats", __name__)

# API endpoint for ATS check
@ats_bp.route("/api/check_ats", methods=["POST"])
def check_ats():
    data = request.json
    resume_text = data.get("resume", "")
    job_desc = data.get("job_description", "")

    # --- Dummy logic: you will replace with real NLP later ---
    score = 72
    suggestions = ["Add Python", "Mention SQL", "Highlight AWS experience"]

    return jsonify({"score": score, "suggestions": suggestions})


# Route to display ATS result page
@ats_bp.route("/ats_result")
def ats_result():
    score = int(request.args.get("score", 0))
    suggestions = request.args.getlist("suggestions")
    return render_template("ats_result.html", score=score, suggestions=suggestions)
