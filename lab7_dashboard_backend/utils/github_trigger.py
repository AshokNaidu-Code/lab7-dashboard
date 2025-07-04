import os
import requests
from dotenv import load_dotenv
from lab7_dashboard_backend.utils.build_log import add_build_entry

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_OWNER = "AshokNaidu-Code"
REPO_NAME = "lab7-dashboard"
WORKFLOW_FILE = "build.yml"
BRANCH = "master"

def trigger_github_action():
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/actions/workflows/{WORKFLOW_FILE}/dispatches"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    payload = {"ref": BRANCH}

    try:
        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 204:
            status = "success"
            msg = "✅ GitHub Action triggered successfully!"
        else:
            status = "failed"
            msg = f"❌ GitHub error {response.status_code}: {response.text}"

    except Exception as e:
        status = "failed"
        msg = f"❌ Request exception: {str(e)}"
        response = None

    try:
        add_build_entry(status, msg)
    except Exception as log_err:
        print("⚠️ Failed to log build:", log_err)

    return {
        "status": response.status_code if response else 500,
        "message": msg
    }