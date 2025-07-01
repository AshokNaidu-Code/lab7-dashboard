from fastapi import FastAPI
from api.trigger import router as trigger_router

app = FastAPI()
app.include_router(trigger_router, prefix="/trigger")