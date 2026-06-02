from pydantic import BaseModel
from typing import Dict

class ModerationRequest(BaseModel):
    text: str

class ModerationResponse(BaseModel):
    text: str
    flagged: bool
    top_category: str
    confidence: float          
    all_scores: Dict[str, float] 
    severity: str              
