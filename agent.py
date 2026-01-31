import os
from exa_py import Exa

exa = Exa(api_key=os.getenv("EXA_API_KEY"))

def run_recruiting_agent(payload: dict):
    criteria = payload.get("criteria", "").strip()

    if not criteria:
        return {"error": "No criteria provided"}

    webset_failure = None
    search_failure = None

    # -----------------------------
    # 1. PRIMARY: Websets (SDK-safe)
    # -----------------------------
    try:
        # Step 1: create empty webset
        webset = exa.websets.create()

        # Step 2: add search to webset
        exa.websets.search(
            webset_id=webset.id,
            query=criteria,
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

    except Exception as e:
        webset_failure = str(e)

    # -----------------------------
    # 2. FALLBACK: Search API
    # -----------------------------
    try:
        search_results = exa.search(
            query=criteria,
            num_results=3
        )

        if search_results.results:
            return {
                "source": "search
