from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Philippine Church Directory API is running."}