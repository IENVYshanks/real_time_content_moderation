import re
import os
from dotenv import load_dotenv
from src.models.model_response import ModerationResponse

load_dotenv()

CONTENT_MODERATION_REGEX = re.compile(
    r"""
    \b(
        fuck|fucking|fucker|motherfucker|
        shit|bullshit|shitty|
        bitch|bitches|
        asshole|ass|bastard|
        dick|dickhead|cock|
        pussy|cunt|
        slut|whore|
        retard|idiot|moron|
        loser|stupid|dumbass|
        nigga|nigger|
        faggot|gaylord|
        kill\s+yourself|kys|
        suicide|self[- ]?harm|
        nazi|hitler|
        terrorist|terrorism|
        rape|rapist|
        pedophile|pedo|
        sexcam|onlyfans|
        scam|fraud|
        drugs?|weed|marijuana|cocaine|heroin|
        gambling|casino
    )\b
    |
    https?://\S+                           # URLs
    |
    www\.\S+                              # URLs without protocol
    |
    [A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,} # Emails
    |
    \b\d{10,}\b                           # Long numbers
    |
    (.)\1{5,}                             # Repeated characters
    """,
    re.IGNORECASE | re.VERBOSE
)

def moderate(text: str) -> bool:
    return not bool(CONTENT_MODERATION_REGEX.search(text))


LABELS = [
    "toxic",
    "severe_toxic",
    "obscene",
    "threat",
    "insult",
    "identity_hate",
]

MODEL_NAME = os.getenv("MODEL_NAME", "unitary/toxic-bert")
FLAGGED_THRESHOLD = float(os.getenv("FLAGGED_THRESHOLD", "0.5"))
MAX_LENGTH = int(os.getenv("MAX_LENGTH", "512"))
MODEL_LOCAL_FILES_ONLY = os.getenv("MODEL_LOCAL_FILES_ONLY", "false").lower() == "true"

_model_resources = None

def load_model() -> None:
    global _model_resources

    if _model_resources is not None:
        return

    import torch
    from transformers import AutoModelForSequenceClassification, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_NAME,
        local_files_only=MODEL_LOCAL_FILES_ONLY,
    )
    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME,
        local_files_only=MODEL_LOCAL_FILES_ONLY,
    )
    model.eval()
    _model_resources = torch, tokenizer, model

def _get_model_resources():
    if _model_resources is None:
        load_model()
    return _model_resources

def _severity(score: float) -> str:
    if score >= 0.85:
        return "high"
    elif score >= 0.5:
        return "medium"
    return "low"

def moderate_text(text: str) -> ModerationResponse:
    regex_flagged = not moderate(text)
    torch, tokenizer, model = _get_model_resources()
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=MAX_LENGTH,
        padding=True,
    )

    with torch.no_grad():
        logits = model(**inputs).logits  

    probs = torch.sigmoid(logits).squeeze().tolist()

    all_scores = {
        label: round(float(prob), 4)
        for label, prob in zip(LABELS, probs)
    }

    top_category = max(all_scores, key=all_scores.get)
    confidence = all_scores[top_category]
    flagged = regex_flagged or confidence >= FLAGGED_THRESHOLD

    if regex_flagged and confidence < 1.0:
        all_scores["regex"] = 1.0
        top_category = "regex"
        confidence = 1.0

    return ModerationResponse(
        text=text,
        flagged=flagged,
        top_category=top_category,
        confidence=confidence,
        all_scores=all_scores,
        severity=_severity(confidence),
    )
