# This is code copied directly from the cybersectony homepage found at https://huggingface.co/ealvaradob/bert-finetuned-phishing
# I am not the original creator of the following code

import os
os.environ['HF_TOKEN'] = 'YOUR_TOKEN_HERE'
from huggingface_hub import InferenceClient
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

# Use a pipeline as a high-level helper
pipe = pipeline("text-classification", model="ealvaradob/bert-finetuned-phishing")

# Load model directly
tokenizer = AutoTokenizer.from_pretrained("ealvaradob/bert-finetuned-phishing")
model = AutoModelForSequenceClassification.from_pretrained("ealvaradob/bert-finetuned-phishing")

client = InferenceClient(
    provider="auto",
    api_key=os.environ["HF_TOKEN"],
)

result = client.text_classification(
    "I like you. I love you",
    model="ealvaradob/bert-finetuned-phishing",
)