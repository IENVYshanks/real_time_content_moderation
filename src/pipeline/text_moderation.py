from src.models.user_text import UserText
from src.utils.regex import moderate

def text_pipeline(text: UserText) -> bool:
    if(moderate(text.text)){
        
    }
    return False