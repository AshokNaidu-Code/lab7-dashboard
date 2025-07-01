from fastapi import APIRouter
from utils.github_trigger import trigger_github_action

router = APIRouter()

@router.post("/")
async def run_pipeline():
    result = await trigger_github_action()
    return result