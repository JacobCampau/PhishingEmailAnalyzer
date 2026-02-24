from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from transformers_interpret import SequenceClassificationExplainer

# Load the model and tokenizer from Hugging Face Hub
model_id = "aamoshdahal/email-phishing-distilbert-finetuned"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForSequenceClassification.from_pretrained(model_id)

# Set device (GPU if available)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
model.eval()

# Example email for prediction
#email = """Dear user,

#We detected suspicious activity on your account. Please verify your identity immediately by clicking the link below to avoid suspension.

#[Phishing Link Here]

#Thank you,
#Security Team"""

# Tokenize and prepare the input
#encoded_input = tokenizer(email, return_tensors='pt', truncation=True, padding=True).to(device)

# Make prediction
#with torch.no_grad():
#    outputs = model(**encoded_input)
#    probs = torch.nn.functional.softmax(outputs.logits, dim=1)

# Output prediction
#labels = ["legitimate", "phishing"]
#pred_label = labels[probs.argmax()]
#confidence = probs.max().item()

#print(f"Prediction: {pred_label} ({confidence:.2%} confidence)")

#explainer = SequenceClassificationExplainer(model=model, tokenizer=tokenizer)
#word_attributions = explainer(email, class_name="LABEL_0")
#explainer.visualize()