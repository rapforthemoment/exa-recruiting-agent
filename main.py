from fastapi import FastAPI, Header, HTTPException
from agent import run_recruiting_agent

app = FastAPI()

@app.post("/search")
def search(payload: dict, x_wp_key: str = Header(None)):
    if x_wp_key != "exa_wp_secret_2026":
        raise HTTPException(status_code=401, detail="Unauthorized")

    return run_recruiting_agent(payload)
