from fastapi import APIRouter, HTTPException
from src.models.model_response import ModerationResponse, ModerationRequest
from src.service.moderation_service import moderate_text

router = APIRouter(prefix="/moderate", tags=["moderation"])

@router.post("/", response_model=ModerationResponse)
async def moderate(request: ModerationRequest) -> ModerationResponse:
    if not request.text.strip():
        raise HTTPException(status_code=422, detail="Text cannot be empty")
    return moderate_text(request.text)
