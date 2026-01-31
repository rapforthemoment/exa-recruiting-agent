import os
from exa_py import Exa

exa = Exa(api_key=os.getenv("EXA_API_KEY"))

def run_recruiting_agent(payload: dict):
    criteria = payload.get("criteria", "").strip()

    if not criteria:
        return {"error": "No criteria provided"}

    # -----------------------------
    # 1. PRIMARY: Websets (FIXED)
    # -----------------------------
    try:
        webset = exa.websets.create(
            prompt=criteria,   # <-- FIXED
            num_results=5
        )

        items = exa.websets.items(webset.id)

        if items and items.items:
            return {
                "source": "websets",
                "criteria": criteria,
                "count": len(items.items),
                "results": [
                    {
                        "name": i.title or "Unknown",
                        "url": i.url,
                        "summary": (i.text or "")[:300]
                    }
                    for i in items.items
                ]
            }

    except Exception as webset_error:
        webset_failure = str(webset_error)
    else:
        webset_failure = None

    # -----------------------------
    # 2. FALLBACK: Search (expected to fail if no credits)
    # -----------------------------
    try:
        search_results = exa.search(
            query=criteria,
            num_results=3
        )

        if search_results.results:
            return {
                "source": "search",
                "criteria": criteria,
                "count": len(search_results.results),
                "results": [
                    {
                        "name": r.title or "Unknown",
                        "url": r.url,
                        "summary": (r.text or "")[:300],
                        "score": r.score
                    }
                    for r in search_results.results
                ]
            }

    except Exception as search_error:
        search_failure = str(search_error)
    else:
        search_failure = None

    return {
        "error": "No results available",
        "criteria": criteria,
        "websets_error": webset_failure,
        "search_error": search_failure
    }
