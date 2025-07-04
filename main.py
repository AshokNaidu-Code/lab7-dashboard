import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://lab7-dashboard.vercel.app"],

    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Detect Railway environment
IN_RAILWAY = os.getenv("RAILWAY_DEPLOYMENT_ID") is not None

if not IN_RAILWAY:
    from lab7_dashboard_backend.api.trigger import router as trigger_router
    app.include_router(trigger_router)
else:
    print("⚠️ Skipping Docker-based routes (Railway environment)")

@app.get("/")
def home():
    return {"message": "✅ Backend is live and running!"}

@app.get("/list")
def get_list():
    return { "containers": [] }