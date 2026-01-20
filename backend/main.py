from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import ProductivityInput
from agent import run_productivity_agent

app = FastAPI(title="AI Personal Productivity Coach")

# -------------------- CORS CONFIG --------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",     # local dev (Vite)
        "http://localhost:3000",     # optional
        "*"                          # allow deployed frontend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------- ROUTES --------------------
@app.get("/")
def read_root():
    return {"status": "AI Productivity Coach backend is running"}

@app.post("/generate-plan")
async def generate_plan(data: ProductivityInput):
    plan = await run_productivity_agent(data)
    return plan
