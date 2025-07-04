import os
from fastapi import FastAPI

app = FastAPI()

# Detect Railway environment
IN_RAILWAY = os.getenv("RAILWAY_DEPLOYMENT_ID") is not None

if not IN_RAILWAY:
    from lab7_dashboard_backend.api.trigger import router as trigger_router
    app.include_router(trigger_router)
else:
    print("⚠️ Skipping Docker-based routes (Railway environment)")