import os
import httpx
from dotenv import load_dotenv

load_dotenv()

async def trigger_github_action():
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    GITHUB_REPO = os.getenv("GITHUB_REPO")

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    url = f"https://api.github.com/repos/{GITHUB_REPO}/dispatches"
    payload = { "event_type": "lab7-manual-trigger" }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload)
        return {
            "status": response.status_code,
            "message": "Build triggered" if response.status_code == 204 else response.text
        }