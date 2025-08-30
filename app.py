from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, current_user
from database import db
from models import User
from config import Config
from auth import auth_bp
from resumes import resumes_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Extensions
    db.init_app(app)

    # Auth
    login_manager = LoginManager()
    login_manager.login_view = "auth.login_get"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(resumes_bp)

    @app.get("/")
    def index():
        # Landing page
        return render_template("index.html")

    # Create tables on first run
    with app.app_context():
        db.create_all()

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
