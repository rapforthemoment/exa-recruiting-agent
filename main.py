import os
from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from exa_py import Exa

# -----------------------------
# App
# -----------------------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Secrets
# -----------------------------
EXA_API_KEY = os.getenv("EXA_API_KEY")
WP_SHARED_SECRET = "exa_wp_secret_2026"

if not EXA_API_KEY:
    raise RuntimeError("EXA_API_KEY missing")

exa = Exa(api_key=EXA_API_KEY)

# -----------------------------
# Models
# -----------------------------
class SearchRequest(BaseModel):
    criteria: str

# -----------------------------
# Routes
# -----------------------------
@app.post("/search")
async def search(
    payload: SearchRequest,
    x_wp_key: str = Header(None)
):
    if x_wp_key != WP_SHARED_SECRET:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        response = exa.search(
            query=payload.criteria,
            num_results=10
        )

        results = []
        for r in response.results:
            results.append({
                "title": r.title,
                "url": r.url,
                "snippet": r.snippet
            })

        return {
            "criteria": payload.criteria,
            "count": len(results),
            "results": results
        }

    except Exception as e:
        return {
            "error": "Search failed",
            "details": str(e)
        }

@app.get("/")
def root():
    return {"status": "ok"}
