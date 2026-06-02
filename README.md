# RTCM

FastAPI service for text moderation. The app combines a regex blocklist with the
`unitary/toxic-bert` Hugging Face model and returns category scores plus a final
flagged decision.

## Setup

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Create your local environment file:

```powershell
Copy-Item .env.example .env
```

Environment variables:

- `MODEL_NAME`: Hugging Face model id or local model path.
- `FLAGGED_THRESHOLD`: model score threshold used to flag text.
- `MAX_LENGTH`: tokenizer max sequence length.
- `MODEL_LOCAL_FILES_ONLY`: set to `true` to require an already-cached/local model.

## Run

Start the API:

```powershell
.\.venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000
```

The Toxic-BERT model loads during FastAPI startup. On the first run, the app
needs network access to download `unitary/toxic-bert`; after that it uses the
local Hugging Face cache.

## Endpoints

Health check:

```http
GET /main
```

Text moderation:

```http
POST /moderate/
Content-Type: application/json

{
  "text": "hello"
}
```

Example response:

```json
{
  "text": "hello",
  "flagged": false,
  "top_category": "toxic",
  "confidence": 0.0009,
  "all_scores": {
    "toxic": 0.0009,
    "severe_toxic": 0.0001,
    "obscene": 0.0002,
    "threat": 0.0001,
    "insult": 0.0002,
    "identity_hate": 0.0001
  },
  "severity": "low"
}
```

Blank text returns `422`.

## Development Notes

- Main app entrypoint: `main.py`
- Router: `src/router/text_ingesation.py`
- Request/response schemas: `src/models/model_response.py`
- Moderation logic and model loading: `src/service/moderation_service.py`
