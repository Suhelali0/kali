from fastapi import APIRouter
from backend.services.email_service import scan_email

router = APIRouter()

@router.post("/scan")
def scan(data: dict):
    return scan_email(data["sender"], data["subject"], data["body"])
