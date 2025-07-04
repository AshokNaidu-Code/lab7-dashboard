from fastapi import APIRouter, Request
from pydantic import BaseModel
from lab7_dashboard_backend.utils.build_log import get_build_history, clear_history, add_build_entry
from lab7_dashboard_backend.utils.github_trigger import trigger_github_action
from lab7_dashboard_backend.api.docker_utils import list_running_containers, stop_containers_by_image
import subprocess
import os
from datetime import datetime
import shutil

router = APIRouter()

class StopRequest(BaseModel):
    image: str

class ImageRequest(BaseModel):
    image: str

DOCKER_CLI = shutil.which("docker") or r"C:\Program Files\Docker\Docker\resources\bin\docker.exe"

@router.post("/trigger/")
def trigger():
    return trigger_github_action()

@router.get("/trigger/history")
def get_history():
    return get_build_history()

@router.post("/trigger/history/clear")
def wipe():
    clear_history()
    return {"message": "Logs cleared"}

@router.post("/trigger/docker/")
def build_docker_image():
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    image_tag = f"ashoknallam/lab7-dashboard:{timestamp}"
    try:
        cwd_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        result = subprocess.run(
            [DOCKER_CLI, "build", "-t", image_tag, "."],
            capture_output=True,
            text=True,
            encoding="utf-8",
            cwd=cwd_path
        )
        if result.returncode == 0:
            msg = f"✅ Docker build successful: {image_tag}"
            push = subprocess.run(
                [DOCKER_CLI, "push", image_tag],
                capture_output=True,
                text=True
            )
            if push.returncode == 0:
                msg += "\n🚀 Pushed to Docker Hub"
            else:
                msg += f"\n❌ Push failed:\n{push.stderr}"
            status = "success"
        else:
            msg = f"❌ Build failed:\n{result.stderr}"
            status = "failed"
    except Exception as e:
        msg = f"⚠️ Exception during build: {str(e)}"
        status = "failed"
        image_tag = None

    add_build_entry(status, msg)
    return {"status": status, "message": msg, "image_tag": image_tag}

@router.post("/trigger/docker/run/")
def run_container(req: ImageRequest):
    image = req.image
    try:
        result = subprocess.run(
            [DOCKER_CLI, "run", "-d", "-p", "8000:8000", image],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            msg = f"🟢 Running container from {image}"
            status = "success"
        else:
            msg = f"❌ Failed to launch container:\n{result.stderr}"
            status = "failed"
    except Exception as e:
        msg = f"⚠️ Exception while running: {str(e)}"
        status = "failed"

    add_build_entry(status, msg)
    return {"status": status, "message": msg}

@router.post("/trigger/docker/stop/")
async def stop_container(req: StopRequest):
    image = req.image.strip()
    return stop_containers_by_image(image)

@router.get("/trigger/docker/list/")
def list_containers():
    return list_running_containers()