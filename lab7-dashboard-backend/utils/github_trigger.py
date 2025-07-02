import os
import httpx
from dotenv import load_dotenv
from .build_log import add_build_entry
import requests

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


async def trigger_github_action():
    try:
        response = requests.post(
            "https://api.github.com/repos/AshokNaidu-Code/lab7-dashboard/actions/workflows/build.yml/dispatches",
            headers={
                "Authorization": f"Bearer {GITHUB_TOKEN}",
                "Accept": "application/vnd.github+json"
            },
            json={"ref": "main"}
        )

        if response.status_code == 204:
            msg = "Build triggered!"
            status = "success"
        else:
            msg = response.text
            status = "failed"

    except Exception as e:
        msg = f"Request failed: {str(e)}"
        status = "failed"
        response = None  # <- ensures the variable exists

    add_build_entry(status, msg)

    return {
        "status": response.status_code if response else 500,
        "message": msg
    }


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