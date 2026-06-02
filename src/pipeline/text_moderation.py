from src.models.user_text import UserText
from src.utils.regex import moderate

def text_pipeline(text: str) -> bool:
    if(moderate(text)):
        pass
    return True