from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import os

# Get the locally saved model file path
# no longer used as the models load straight from hugging face. The code here is kept for future reference
from pathlib import Path
MODEL_PATH = Path(__file__).resolve().parent / "models" / "ealvaradob"

# set model id from Hugging Face
MODEL_ID = "ealvaradob/bert-finetuned-phishing"
HF_TOKEN = os.getenv("HUGGINGFACE_HUB_TOKEN")

# set the tokenizer and device from the model id
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, token = HF_TOKEN)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu") # attempt to use the GPU

# set-up model
model = AutoModelForSequenceClassification.from_pretrained(MODEL_ID, token = HF_TOKEN)
model.to(device)
model.eval()

def predict(email: str):
    # email body and url detection
    encoded_email = tokenizer(
        email,
        return_tensors = "pt",
        truncation = True,
        padding = True
    ).to(device)
    
    # make prediction
    with torch.no_grad():
        outputs = model(**encoded_email)
        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)

    # output prediction
    labels = ["legitimate", "phishing"]
    pred_label = labels[probs.argmax()]
    confidence = probs.max().item()

    return {
        "labels": labels,
        "probs": probs,
        "model_id": MODEL_ID,
        "pred": pred_label,
        "confidence": confidence
    }