from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import os

# Get the locally saved model file path
from pathlib import Path
MODEL_PATH = Path(__file__).resolve().parent / "models" / "cybersectony"

# # get the hf token from the environment
# HF_TOKEN = os.getenv("HUGGINGFACE_HUB_TOKEN")

# set model id from Hugging Face
MODEL_ID = "cybersectony/phishing-email-detection-distilbert_v2.4.1"

# set the tokenizer and device from the model id
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, local_files_only=True)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu") # attempt to use the GPU

# set-up model
# MODEL_ID, token = HF_TOKEN
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH, local_files_only=True)
model.to(device)
model.eval()

def predict(email: str):
    # email body and url detection
    encoded_email = tokenizer(
        email,
        return_tensors="pt",
        truncation=True,
        max_length=512
    ).to(device)
    
    # make prediction
    with torch.no_grad():
        outputs = model(**encoded_email)
        predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
    
    # following differs from other models to better match its hugging face documented code
    # model probs
    probs = predictions[0].tolist()
    
    # url and body outputs
    labels = {
        "legitimate_email": probs[0],
        "phishing_url": probs[1],
        "legitimate_url": probs[2],
        "phishing_url_alt": probs[3]
    }
    
    # results
    pred_label = max(labels.items(), key=lambda x: x[1])
    confidence = predictions.max().item()

    return {
        "labels": labels,
        "probs": probs,
        "model_id": MODEL_ID,
        "pred": pred_label[0],
        "confidence": confidence
    }
