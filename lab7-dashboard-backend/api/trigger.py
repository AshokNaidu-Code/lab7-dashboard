from fastapi import APIRouter
from utils.github_trigger import trigger_github_action
from utils.build_log import get_build_history, clear_history

router = APIRouter()

@router.post("/")
async def run_pipeline():
    result = await trigger_github_action()
    return result

@router.post("/trigger/")
def trigger():
    return trigger_github_action()

@router.get("/history")
async def build_history():
    return get_build_history()

@router.get("/trigger/history")
def get_history():
    return get_build_history()

@router.post("/trigger/history/clear")
def wipe_history():
    clear_history()
    return {"message": "Log history cleared."}
