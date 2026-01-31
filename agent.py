import os
from exa_py import Exa

exa = Exa(api_key=os.getenv("EXA_API_KEY"))

def run_recruiting_agent(payload: dict):
    criteria = payload.get("criteria")

    if not criteria:
        return {
            "error": "No criteria provided"
        }

    try:
        webset = exa.websets.create(
            {
                "query": criteria,
                "entity_type": "person",
                "num_results": 10
            }
        )

        results = []

        for r in webset.results:
            results.append({
                "name": r.get("name"),
                "url": r.get("url"),
                "description": r.get("description"),
                "source": r.get("source")
            })

        return {
            "criteria": criteria,
            "count": len(results),
            "results": results
        }

    except Exception as e:
        return {
            "error": "Websets failed",
            "details": str(e)
        }
