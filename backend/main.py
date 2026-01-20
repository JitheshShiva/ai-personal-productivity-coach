from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import ProductivityInput
from agent import run_productivity_agent

app = FastAPI()

# CORS FIX
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "AI Productivity Coach backend is running"}

@app.post("/generate-plan")
async def generate_plan(data: ProductivityInput):
    plan = await run_productivity_agent(data)
    return plan
