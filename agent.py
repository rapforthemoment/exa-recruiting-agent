import os
from exa_py import Exa

exa = Exa(api_key=os.getenv("EXA_API_KEY"))

def run_recruiting_agent(payload: dict):
    """
    payload example:
    {
        "criteria": "wordpress design experts based in the US and have management experience"
    }
    """

    criteria = payload.get("criteria", "")

    if not criteria:
        return {
            "error": "No criteria provided"
        }

    # 1. Search for relevant people/pages
    search_results = exa.search(
        query=criteria,
        num_results=5,
        exclude_domains=[
            "facebook.com",
            "twitter.com",
            "instagram.com",
            "youtube.com"
        ]
    )

    candidates = []

    # 2. Convert Exa results into structured candidates
    for r in search_results.results:
        candidates.append({
            "name": r.title or "Unknown",
            "profile_url": r.url,
            "snippet": r.text[:300] if r.text else "",
            "source": r.domain,
            "score": round(r.score, 2) if r.score else None
        })

    # 3. Return structured data
    return {
        "criteria": criteria,
        "count": len(candidates),
        "results": candidates
    }

