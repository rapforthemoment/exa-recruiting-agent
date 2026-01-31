from fastapi import FastAPI, Header, HTTPException
from agent import run_recruiting_agent

app = FastAPI()

@app.post("/recruit")
def recruit(payload: dict, x_wp_key: str = Header(None)):
    if x_wp_key != "replace-this-with-your-own-secret":
        raise HTTPException(status_code=401, detail="Unauthorized")

    result = run_recruiting_agent(payload)
    return result

