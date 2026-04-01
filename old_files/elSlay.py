from transformers import BertForSequenceClassification, BertTokenizer
import torch
import os

# get the hf token from the environment
HF_TOKEN = os.getenv("HUGGINGFACE_HUB_TOKEN")

# set model id from Hugging Face
MODEL_ID = "ElSlay/BERT-Phishing-Email-Model"

# set the tokenizer and device from the model id
tokenizer = BertTokenizer.from_pretrained(MODEL_ID, token = HF_TOKEN)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu") # attempt to use the GPU

# set-up model
model = BertForSequenceClassification.from_pretrained(MODEL_ID, token = HF_TOKEN)
model.to(device)
model.eval()

def predict(email: str):
    # email body and url detection
    encoded_email = tokenizer(
        email,
        return_tensors = "pt",
        truncation = True,
        padding = 'max_length',
        max_length = 512
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