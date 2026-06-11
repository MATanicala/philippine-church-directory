from fastapi import FastAPI
from app.core.database import engine
from app.models.base import Base
from app.models import church  # Ensures the Church model metadata is loaded
from app.routes import church_routes # Import the church routes

app = FastAPI(
    title="Philippine Church Directory API",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)

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

# Include the church routes in the main application
app.include_router(church_routes.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Church Directory API"}