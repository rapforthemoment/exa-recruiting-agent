import os
from exa_py import Exa
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

# ---------------------------------------------
# Setup
# ---------------------------------------------

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

exa = Exa(api_key=os.environ.get("EXA_API_KEY"))

# ---------------------------------------------
# Utility: filter junk results
# ---------------------------------------------

JUNK_KEYWORDS = [
    "top ",
    "best ",
    "list ",
    "comparison",
    "vs ",
    "ranking",
    "review",
    "directory",
    "companies in",
]

JUNK_DOMAINS = [
    "clutch.co",
    "upwork.com",
    "fiverr.com",
    "goodfirms.co",
    "designrush.com",
    "promotedigital.com",
    "blog.",
    "medium.com",
]

def is_junk(result):
    title = (result.title or "").lower()
    url = (result.url or "").lower()

    for kw in JUNK_KEYWORDS:
        if kw in title:
            return True

    for domain in JUNK_DOMAINS:
        if domain in url:
            return True

    return False

# ---------------------------------------------
# Main recruiting search
# ---------------------------------------------

def run_recruiting_agent(criteria: str):
    search = exa.search(
        query=criteria,
        num_results=20,
        type="neural",
    )

    cleaned_results = []

    for r in search.results:
        if is_junk(r):
            continue

        cleaned_results.append({
            "title": r.title,
            "url": r.url,
            "snippet": r.text[:400] if r.text else None,
            "source": r.url.split("/")[2] if "://" in r.url else r.url,
            "score": r.score,
        })

    return {
        "criteria": criteria,
        "count": len(cleaned_results),
        "results": cleaned_results
    }

# ---------------------------------------------
# API endpoint
# ---------------------------------------------

@app.post("/search")
async def search_endpoint(request: Request):
    body = await request.json()
    criteria = body.get("criteria")

    if not criteria:
        return {"error": "Missing criteria"}

    try:
        return run_recruiting_agent(criteria)
    except Exception as e:
        return {
            "error": "Search failed",
            "details": str(e)
        }
