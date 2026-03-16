from transformers import BertTokenizerFast, BertForSequenceClassification, pipeline
import torch

# set model id from Hugging Face
MODEL_ID = "CrabInHoney/urlbert-tiny-v4-phishing-classifier"

# set the tokenizer and device from the model id
tokenizer = BertTokenizerFast.from_pretrained(MODEL_ID)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu") # attempt to use the GPU
device_num = 0 if torch.cuda.is_available() else -1

# set-up model
model = BertForSequenceClassification.from_pretrained(MODEL_ID)
model.to(device)
model.eval()

def predict_url(url: str):
    # This mode only is used for testing urls
    encoded_url = tokenizer(
        url,
        return_tensors = 'pt',
        truncation = True,
        max_length = 64
    ).to(device)

    with torch.no_grad():
        output = _model(**encoded_url)
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