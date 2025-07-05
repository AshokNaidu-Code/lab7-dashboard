import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from lab7_dashboard_backend.api.trigger import router as trigger_router

app = FastAPI()

# ✅ Include all routes, regardless of env
app.include_router(trigger_router)

# ✅ Allow fetches from your deployed frontend (on Vercel)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://lab7-dashboard.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "✅ Backend is live and running!"}

@app.get("/list")
def list_containers():
    if not shutil.which("docker"):
        return {
            "warning": "🚫 Docker CLI not available in this environment.",
            "containers": [
                { "id": "abc123", "image": "nginx", "status": "Exited (mock)" },
                { "id": "def456", "image": "mongo", "status": "Up 5 hours (mock)" }
            ]
        }



# ✅ Logs all loaded routes (visible in Railway logs)
for route in app.routes:
    print(f"🔗 Route active: {route.path}")