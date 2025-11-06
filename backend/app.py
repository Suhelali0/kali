from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


# Import routers
from backend.routers.analysis import router as explain_router
from backend.routers.file_router import router as file_router
from backend.routers.email_router import router as email_router

from backend.routers.file_router import router as file_router
app = FastAPI(title="AI Cyber Sentinel - Phase 1+2")

# CORS middleware so frontend (served as file or on different port) can call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     # demo/hackathon friendly; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(url_router, prefix="/api/url", tags=["URL Scanner"])
app.include_router(email_router, prefix="/api/email", tags=["Email Scanner"])
app.include_router(file_router, prefix="/api/file", tags=["File Scanner"])
app.include_router(explain_router)
@app.get("/")
async def root():
    return {"message": "AI Cyber Sentinel backend running (Phase 1 + Phase 2)"}
