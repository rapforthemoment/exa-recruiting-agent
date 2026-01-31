from fastapi import FastAPI
from agent import run_recruiting_agent

app = FastAPI()

@app.post("/recruit")
def recruit(payload: dict):
    return run_recruiting_agent(payload)
