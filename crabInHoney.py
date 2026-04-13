from transformers import BertTokenizerFast, BertForSequenceClassification
import torch

# Get the locally saved model file path
from pathlib import Path
MODEL_PATH = Path(__file__).resolve().parent / "models" / "crabInHoney"

# set model id from Hugging Face
MODEL_ID = "CrabInHoney/urlbert-tiny-v4-phishing-classifier"

# set the tokenizer and device from the model id
tokenizer = BertTokenizerFast.from_pretrained(MODEL_PATH, local_files_only=True)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu") # attempt to use the GPU

# set-up model
model = BertForSequenceClassification.from_pretrained(MODEL_PATH, local_files_only=True)
model.to(device)
model.eval()

def predict_url(url: str):
    # This mode only is used for testing urls
    encoded_url = tokenizer(
        url,
        return_tensors = 'pt',
        truncation = True,
        padding = True,
        max_length = 64
    ).to(device)

    with torch.no_grad():
        output = model(**encoded_url)
        probs = torch.nn.functional.softmax(output.logits, dim=1)

    # Output prediction
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
        "confidence": confidence,
        "url": url
    }