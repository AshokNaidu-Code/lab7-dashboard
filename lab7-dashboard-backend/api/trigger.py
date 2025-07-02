from fastapi import APIRouter
from utils.build_log import get_build_history, clear_history
from utils.github_trigger import trigger_github_action

router = APIRouter()

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