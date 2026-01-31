from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from agent import run_recruiting_agent
from fastapi import Header, HTTPException

app = FastAPI()

# ✅ CORS FIX
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/search")
def search(payload: dict, x_wp_key: str = Header(None)):
    if x_wp_key != "replace-this-with-your-own-secret":
        raise HTTPException(status_code=401, detail="Unauthorized")

    return run_recruiting_agent(payload)
