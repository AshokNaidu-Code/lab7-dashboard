import os

IN_RAILWAY = os.getenv("RAILWAY_DEPLOYMENT_ID") is not None

from fastapi import APIRouter

router = APIRouter()

if not IN_RAILWAY:
    from lab7_dashboard_backend.api.docker_utils import (
        list_running_containers,
        stop_containers_by_image,
    )

    @router.get("/list")
    def list_containers():
        return list_running_containers()

    @router.post("/stop")
    def stop(image_name: str):
        return stop_containers_by_image(image_name)
else:
    @router.get("/list")
    def list_stub():
        return {"warning": "🚫 Docker CLI not available (running inside Railway)"}