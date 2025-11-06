from fastapi import APIRouter
from backend.services.ai_explain import explain_threat

router = APIRouter()

@router.post("/ai_explain")
def explain(data: dict):
    return explain_threat(data["text"], data["detection"])
