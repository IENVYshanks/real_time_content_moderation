import os
from huggingface_hub import InferenceClient

client = InferenceClient(
    provider="hf-inference",
    api_key=os.environ["HF_TOKEN"],
)

def bert_moderation(text: str) -> bool:
    result = client.text_classification(
        text,
        model="unitary/toxic-bert",
    )
    return result[0].score > 0.5