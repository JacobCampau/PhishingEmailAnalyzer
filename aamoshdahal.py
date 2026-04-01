from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import os

# Get the locally saved model file path
from pathlib import Path
MODEL_PATH = Path(__file__).resolve().parent / "models" / "aamoshdahal"

# # get the hf token from the environment
# HF_TOKEN = os.getenv("HUGGINGFACE_HUB_TOKEN")

# set model id from Hugging Face
MODEL_ID = "aamoshdahal/email-phishing-distilbert-finetuned"

# set the tokenizer and device from the model id
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, local_files_only=True)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu") # attempt to use the GPU

# set-up model
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH, local_files_only=True)
model.to(device)
model.eval()

def predict(email: str):
    # code based off hugging face model page
    # email body detection only
    encoded_email = tokenizer(
        email, 
        return_tensors = 'pt', 
        truncation = True, 
        padding = True
    ).to(device)

    # make prediction
    with torch.no_grad():
        output = model(**encoded_email)
        probs = torch.nn.functional.softmax(output.logits, dim=1)

    # output prediction
    labels = ["legitimate", "phishing"]
    pred_label = labels[probs.argmax()]
    confidence = probs.max().item()

    return {
        # less important, but still accessable
        "labels": labels,
        "probs": probs,
        # important output results
        "model_id": MODEL_ID,
        "pred": pred_label,
        "confidence": confidence
    }