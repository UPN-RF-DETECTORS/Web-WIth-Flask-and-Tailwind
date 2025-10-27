import os
from flask import send_from_directory

from core.db_config import db
from core.app_config import create_app

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = create_app()
    # ✅ Tambahkan route publik agar bisa akses /public/images
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
