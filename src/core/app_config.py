import os
from flask import Flask
from core.db_config import db

def create_app():
    BASE_DIR = os.path.dirname(os.path.abspath((os.path.abspath(__file__))))
    app = Flask(
        __name__,
        template_folder=os.path.join(BASE_DIR, "../templates"),
        static_folder=os.path.join(BASE_DIR, "../static")
    )

    app.config['SECRET_KEY'] = 'secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/palm_detector_dev'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Register blueprints
    from users.routers import auth_bp
    app.register_blueprint(auth_bp)

    return app
