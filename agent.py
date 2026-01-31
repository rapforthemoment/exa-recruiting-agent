import os
from exa_py import Exa

exa = Exa(api_key=os.getenv("EXA_API_KEY"))


def run_recruiting_agent(payload: dict):
    criteria = payload.get("criteria", "").strip()

    if not criteria:
        return {
            "error": "No criteria provided"
        }

    try:
        webset = exa.websets.create({
            "searches": [
                {
                    "query": criteria,
                    "num_results": 1
                }
            ]
        })

        return {
            "debug": "webset created successfully",
            "criteria": criteria,
            "webset_id": webset.id
        }

    except Exception as e:
        return {
            "error": "Websets failed",
            "details": str(e)
        }
