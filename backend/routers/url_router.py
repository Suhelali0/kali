from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
from services.url_service import analyze_url

router = APIRouter()

class URLRequest(BaseModel):
    url: str  

class URLResponse(BaseModel):
    url: str
    label: str
    score: float
    reason: str

@router.post("/scan", response_model=URLResponse)
async def scan_url(req: URLRequest):
    try:
        result = analyze_url(req.url)
        return {
            "url": result["url"],
            "label": result["label"],
            "score": result["score"],
            "reason": result["reason"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
