from pathlib import Path
from transformers import AutoTokenizer, AutoModelForSequenceClassification

MODEL_DIR = Path(__file__).resolve().parent / "models"

MODEL_IDS = {
    "aamoshdahal": "aamoshdahal/email-phishing-distilbert-finetuned",
    "crabInHoney": "CrabInHoney/urlbert-tiny-v4-phishing-classifier",
    "cybersectony": "cybersectony/phishing-email-detection-distilbert_v2.4.1",
    "ealvardob": "ealvaradob/bert-finetuned-phishing",
}

def load_model(model_name: str, model_id: str):
    file_path = MODEL_DIR / model_name
    file_path.mkdir(parents=True, exist_ok=True)

    print(f"Downloading {model_id} -> {file_path}")
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForSequenceClassification.from_pretrained(model_id)

    tokenizer.save_pretrained(file_path)
    model.save_pretrained(file_path)

    print(f"Saved {model_name} locally.\n")

def main():
    MODEL_DIR.mkdir(exist_ok=True)

    for model_name, model_id in MODEL_IDS.items():
        load_model(model_name, model_id)

if __name__ == "__main__":
    main()