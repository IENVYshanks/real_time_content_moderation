from src.service.moderation_service import moderate

def text_pipeline(text: str) -> bool:
    return moderate(text)
