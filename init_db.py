import pymysql
from app import app
from models import db

def setup_database():
    # Connect directly to MySQL without a specific database to create it first
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    
    try:
        with connection.cursor() as cursor:
            # Create the database if it does not exist
            cursor.execute("CREATE DATABASE IF NOT EXISTS eunika_db")
        connection.commit()
        print("Database 'eunika_db' confirmed/created successfully.")
    except Exception as e:
        print(f"Error creating database: {e}")
    finally:
        connection.close()

    # Now use the Flask app context with SQLAlchemy to create the tables
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")

if __name__ == '__main__':
    setup_database()
