from fastapi import APIRouter, File, UploadFile
from .services.file_service import analyze_file



router = APIRouter()

@router.post("/scan")
async def scan_file(file: UploadFile = File(...)):
    content = await file.read()
    return analyze_file(file.filename, content)
