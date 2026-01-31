from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from agent import run_recruiting_agent

app = FastAPI()

# ✅ CORS FIX (THIS IS THE KEY PART)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later we can lock this to your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/search")
def search(payload: dict, x_wp_key: str = Header(None)):
    if x_wp_key != "exa_wp_secret_2026":
        raise HTTPException(status_code=401, detail="Unauthorized")

    return run_recruiting_agent(payload)
