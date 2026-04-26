from backend.database.config import engine, Base
from backend.models.threat import AttackLog, SessionTrace

def init_db():
    print("Initializing PostgreSQL Database...")
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully.")
    except Exception as e:
        print(f"Error initializing database: {e}")
        print("\nMake sure PostgreSQL is running and the database 'cyphertrap' exists.")
        print("You can create it using: CREATE DATABASE cyphertrap;")

if __name__ == "__main__":
    init_db()
