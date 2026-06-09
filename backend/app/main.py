from fastapi import FastAPI
from app.core.database import engine

app = FastAPI(
    title="Philippine Church Directory API",
    version="1.0.0"
)

@app.on_event("startup")
def test_database_connection():
    """
    Triggers automatically when the server starts.
    Attempts to connect to PostgreSQL to verify credentials.
    """
    try:
        # Try to connect and execute a simple, lightweight query
        with engine.connect() as connection:
            print("Successfully connected to the PostgreSQL database!")
    except Exception as e:
        print("Database connection failed!")
        print(f"Error details: {e}")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Church Directory API"}