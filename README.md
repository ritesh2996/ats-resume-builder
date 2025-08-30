# BeamJobs-Style Resume Builder (Flask + MySQL)

A minimal, production-ready **resume builder** similar in spirit to [BeamJobs](https://www.beamjobs.com/) built with:

- **Backend:** Flask (Python), SQLAlchemy, Flask-Login
- **Frontend:** HTML, CSS, JavaScript (vanilla)
- **DB:** MySQL (JSON column for resume data)
- **PDF Export:** xhtml2pdf (pure Python)

## 1) Prerequisites

- Python 3.10+
- MySQL 5.7+ (or MariaDB 10.2+) with a database created (e.g., `beamjobs_clone`)
- (Optional) A virtualenv tool like `venv` or `conda`

## 2) Create and configure the database

In MySQL shell (or any MySQL client):

```sql
CREATE DATABASE beamjobs_clone CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'beamuser'@'%' IDENTIFIED BY 'strongpassword';
GRANT ALL PRIVILEGES ON beamjobs_clone.* TO 'beamuser'@'%';
FLUSH PRIVILEGES;
```

## 3) Project setup

```bash
cd beamjobs_clone
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
# Edit .env with your MySQL credentials + a strong SECRET_KEY
```

## 4) Run the app (development)

```bash
# Ensure MySQL is running and .env is correct
python app.py
# Visit http://127.0.0.1:5000
```

The first run auto-creates the tables.

## 5) How it works (in simple words)

- **Account:** Users sign up and sign in (email + password). We store password **hashes** (never plaintext).
- **Dashboard:** After login, you click **New Resume** and give it a title (e.g., "Frontend Intern").
- **Editor:** Fill your basics, skills, experience, education, and projects. Click **Save**.
  - The data is stored in the `resumes.data` field as JSON (MySQL JSON column).
- **Preview:** Shows a clean, ATS-friendly layout generated from your JSON.
- **PDF:** Click **Download PDF** to get a professional PDF (via `xhtml2pdf`).

## 6) File structure

```
beamjobs_clone/
  app.py               # Flask app factory + routes registration
  auth.py              # Login, Register, Logout
  resumes.py           # Dashboard, editor, preview, PDF download, JSON save API
  models.py            # User and Resume models
  database.py          # SQLAlchemy setup
  config.py            # Reads .env, builds MySQL URI
  utils/pdf.py         # HTML -> PDF helper
  templates/           # Jinja2 templates (HTML)
  static/css/          # Styles
  static/js/           # Editor logic
  requirements.txt
  .env.example
  README.md
```

## 7) Notes for production

- Set `FLASK_ENV=production`, use a **real** SECRET_KEY.
- Serve with a WSGI server (e.g., `gunicorn`) behind Nginx/Apache.
- Use HTTPS (TLS certificate, e.g., via Let's Encrypt).
- Consider enabling CSRF protection (e.g., Flask-WTF), rate limiting, and detailed logging.
- For fancier PDFs, swap `xhtml2pdf` with `wkhtmltopdf` + `pdfkit` (requires the wkhtmltopdf binary).

## 8) Extending like BeamJobs

- Add **multiple templates** (classic, modern, minimalist) and let users choose in the editor.
- Create a **resume checker** scoring function (keywords, length, action verbs).
- Build a **cover letter** editor with a separate template & PDF.
- Add **job tracking** (company, status, next action) on the dashboard.
- Offer **public share links** for resumes (`/r/<slug>`).

---

MIT-style: do what you want; attribution appreciated.
