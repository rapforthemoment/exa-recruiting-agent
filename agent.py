import os
from exa_py import Exa

exa = Exa(api_key=os.getenv("EXA_API_KEY"))

def run_recruiting_agent(payload: dict):
    criteria = payload.get("criteria")

    if not criteria:
        return {"error": "No criteria provided"}

    try:
        search = exa.search(
            query=criteria,
            num_results=10,
            exclude_domains=[
                "facebook.com",
                "twitter.com",
                "instagram.com",
                "youtube.com"
            ]
        )

        results = []
        for r in search.results:
            results.append({
                "title": r.title,
                "url": r.url,
                "snippet": r.text[:300] if r.text else "",
                "source": r.domain,
                "score": r.score
            })

        return {
            "criteria": criteria,
            "count": len(results),
            "results": results
        }

    except Exception as e:
        return {
            "error": "Search failed",
            "details": str(e)
        }
