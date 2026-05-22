from app import app
from models import db

def setup_database():
    # Now use the Flask app context with SQLAlchemy to create the tables
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")

if __name__ == '__main__':
    setup_database()
