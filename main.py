import os
from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from exa_py import Exa

# --------------------
# ENVIRONMENT
# --------------------
EXA_API_KEY = os.getenv("EXA_API_KEY")
WP_SECRET = os.getenv("WP_SECRET")

if not EXA_API_KEY:
    raise RuntimeError("EXA_API_KEY not set")

if not WP_SECRET:
    raise RuntimeError("WP_SECRET not set")

exa = Exa(EXA_API_KEY)

# --------------------
# FASTAPI APP
# --------------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------
# REQUEST MODEL
# --------------------
class SearchRequest(BaseModel):
    criteria: str

# --------------------
# ROUTES
# --------------------
@app.post("/search")
async def search(
    payload: SearchRequest,
    x_wp_key: str = Header(None)
):
    # Auth check
    if x_wp_key != WP_SECRET:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        results = exa.search(
            query=payload.criteria,
            num_results=10
        )

        formatted = []

        for r in results.results:
            # SAFE extraction — no crashes
            text = ""
            if hasattr(r, "text") and r.text:
                text = r.text
            elif hasattr(r, "highlights") and r.highlights:
                text = " ".join(r.highlights)

            formatted.append({
                "title": r.title,
                "url": r.url,
                "summary": text[:500] if text else ""
            })

        return {
            "criteria": payload.criteria,
            "count": len(formatted),
            "results": formatted
        }

    except Exception as e:
        return {
            "error": "Search failed",
            "details": str(e)
        }
