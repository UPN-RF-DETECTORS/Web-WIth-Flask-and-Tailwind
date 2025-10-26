from core.db_config import db
from core.app_config import create_app


app = create_app()


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
