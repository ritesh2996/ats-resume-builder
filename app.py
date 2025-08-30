import os
from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_login import LoginManager, current_user
from dotenv import load_dotenv
import google.generativeai as genai

from database import db
from models import User
from config import Config
from auth import auth_bp
from resumes import resumes_bp
from ats import ats_bp   # ⬅️ NEW ATS blueprint

# ✅ Load environment variables
load_dotenv()

# ✅ Configure Gemini API once
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # --- Extensions ---
    db.init_app(app)

    # --- Auth ---
    login_manager = LoginManager()
    login_manager.login_view = "auth.login_get"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # --- Blueprints ---
    app.register_blueprint(auth_bp)
    app.register_blueprint(resumes_bp)
    app.register_blueprint(ats_bp)

    @app.get("/")
    def index():
        # Landing page
        return render_template("index.html")

    # 🔹 Chatbot API route
    @app.post("/chatbot")
    def chatbot():
        try:
            user_message = request.json.get("message", "").strip()
            if not user_message:
                return jsonify({"reply": "⚠️ Please enter a message."}), 400

            # ✅ Use Gemini model (fast + reliable)
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(user_message)

            # ✅ Extract reply safely
            reply = response.text if response and response.text else "⚠️ No response from Gemini."

            return jsonify({"reply": reply})

        except Exception as e:
            print("Gemini API Error:", e)
            return jsonify({"reply": f"⚠️ Error: {str(e)}"}), 500

    # --- Database create tables ---
    with app.app_context():
        db.create_all()

    return app

# --- Main entry ---
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
