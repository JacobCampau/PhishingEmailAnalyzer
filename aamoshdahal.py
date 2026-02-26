from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# set model id from Hugging Face
MODEL_ID = "aamoshdahal/email-phishing-distilbert-finetuned"

# set the tokenizer and device from the model id
_tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
_device = torch.device("cuda" if torch.cuda.is_available() else "cpu") # attempt to use the GPU

# set-up model
_model = AutoModelForSequenceClassification.from_pretrained(MODEL_ID)
_model.to(_device)
_model.eval()

def predict(email: str):
    # code based off hugging face model page
    # tokenize input
    encoded_email = _tokenizer(email, return_tensors = 'pt', truncation = True, padding = True).to(_device)

    # Make prediction
    with torch.no_grad():
        output = _model(**encoded_email)
        probs = torch.nn.functional.softmax(output.logits, dim=1)

    # Output prediction
    labels = ["legitimate", "phishing"]
    pred_label = labels[probs.argmax()]
    confidence = probs.max().item()

    return {
        # less important, but still accessable
        "label": labels,
        "probs": probs,
        # important output results
        "model_id": MODEL_ID,
        "pred": pred_label,
        "confidence": confidence
    }

### Left over code from huggin face, DELETE if never used
# from transformers_interpret import SequenceClassificationExplainer # Used in Hugging Face example code at the bottom of file
# explainer = SequenceClassificationExplainer(model=model, tokenizer=tokenizer)
# word_attributions = explainer(email, class_name="LABEL_0")
# explainer.visualize()