import os
from flask import (Flask,send_from_directory,session,redirect,url_for)
from datetime import timedelta
from core.db_config import db

def create_app():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # -> naik 1 folder dari /core ke /src
    app = Flask(
        __name__,
        template_folder=os.path.join(BASE_DIR, "templates"),
        static_folder=os.path.join(BASE_DIR, "static")
    )

    app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "supersecurekey123")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/palm_detector_dev'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10) 
    app.config["UPLOAD_FOLDER"] = os.path.join(BASE_DIR, "static", "uploads")
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    db.init_app(app)

    # Register blueprints
    from users.routers import auth_bp
    from post.routers import post_bp
    from market.routers import trend_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(post_bp)
    app.register_blueprint(trend_bp)
    @app.route('/public/<path:filename>')
    def public_files(filename):
        public_dir = os.path.join(BASE_DIR, 'public')
        return send_from_directory(public_dir, filename)
    # buatkan server error handele
    @app.errorhandler(500)
    def handle_server_error(e):
        session.clear()  # Auto logout saat error
        return redirect(url_for('auth_bp.login_page'))
    return app
