from fastapi import FastAPI
from lab7_dashboard_backend.api.trigger import router as trigger_router
from fastapi.middleware.cors import CORSMiddleware
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'lab7_dashboard_backend'))

print("📂 Current files:", os.listdir())


app = FastAPI()

if not os.getenv("IN_DOCKER"):
    from api.docker_utils import list_running_containers, stop_containers_by_image

from api.trigger import router as trigger_router
app.include_router(trigger_router)


# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 👈 During development only; lock down later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(trigger_router)

@app.get("/")
def root():
    return {"message": "🚀 Lab7 Dashboard container is alive"}

import shutil
print("🧪 Docker path from Python:", shutil.which("docker"))