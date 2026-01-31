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
    # --------------------
    # AUTH CHECK
    # --------------------
    if x_wp_key != WP_SECRET:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        # --------------------
        # STEP 4: EXPERT-FOCUSED QUERY
        # --------------------
        expert_query = f"""
        {payload.criteria}

        site:linkedin.com OR site:scholar.google.com OR site:about.me
        OR site:researchgate.net OR site:medium.com

        "researcher" OR "engineer" OR "consultant"
        OR "author" OR "PhD" OR "founder"
        """

        results = exa.search(
            query=expert_query,
            num_results=10,
            use_autoprompt=True
        )

        # --------------------
        # SAFE RESULT FORMATTING
        # --------------------
        formatted = []

        for r in results.results:
            summary_text = ""

            if hasattr(r, "text") and r.text:
                summary_text = r.text
            elif hasattr(r, "highlights") and r.highlights:
                summary_text = " ".join(r.highlights)

            formatted.append({
                "title": r.title if hasattr(r, "title") else "",
                "url": r.url if hasattr(r, "url") else "",
                "summary": summary_text[:500] if summary_text else ""
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
