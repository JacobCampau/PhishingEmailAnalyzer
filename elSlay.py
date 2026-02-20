from transformers import BertForSequenceClassification, BertTokenizer
import torch

# Replace with your Hugging Face model repo name
model_name = 'ElSlay/BERT-Phishing-Email-Model'

# Load the pre-trained model and tokenizer
model = BertForSequenceClassification.from_pretrained(model_name)
tokenizer = BertTokenizer.from_pretrained(model_name)

# Ensure the model is in evaluation mode
model.eval()

# Use example:
# email_text = "Your email content here"

# # Tokenize and preprocess the input text
# inputs = tokenizer(email_text, return_tensors="pt", truncation=True, padding='max_length', max_length=512)

# # Make the prediction
# with torch.no_grad():
#     outputs = model(**inputs)
#     logits = outputs.logits
#     predictions = torch.argmax(logits, dim=-1)

# # Interpret the prediction
# result = "Phishing" if predictions.item() == 1 else "Legitimate"
# print(f"Prediction: {result}")
