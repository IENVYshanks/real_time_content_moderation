from fastapi import APIRouter 
from src.models.user_text import UserText
from src.pipeline.text_moderation import text_pipeline
router = APIRouter(prefix = "/text_ingestion", tags=["text_ingestion"])

@router.post("/text_ingest")
async def ingest_text(text : UserText):
    is_moderate =text_pipeline(text.text)
    return {"message": text, "is_moderate": is_moderate}