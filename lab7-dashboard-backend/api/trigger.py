from fastapi import APIRouter
from utils.github_trigger import trigger_github_action
from utils.build_log import get_build_history

router = APIRouter()

@router.post("/")
async def run_pipeline():
    result = await trigger_github_action()
    return result

@router.get("/history")
async def build_history():
    return get_build_history()
