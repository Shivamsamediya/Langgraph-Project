from fastapi import FastAPI
from routers import chat
import uvicorn

# Ye hamari main FastAPI application ban rahi hai
app = FastAPI(
    title="LangGraph AI Agent API",
    description="A beginner-friendly FastAPI system using LangGraph and Gemini. Agent can search web and calculate.",
    version="1.0.0"
)

# API router include kar rahe hain jo /api/chat handle karega
app.include_router(chat.router, prefix="/api")

# Ye ek simple health-check route hai
@app.get("/")
def home():
    return {
        "message": "LangGraph Agent API is running! 🚀", 
        "docs": "Visit http://127.0.0.1:8000/docs for Swagger UI to test the API."
    }

if __name__ == "__main__":
    # Ye block tab run hoga jab tum `python main.py` likhoge terminal me
    # reload=True ka matlab code save karte hi server restart hoga
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
