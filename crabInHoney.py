# This is code copied directly from the cybersectony homepage found at https://huggingface.co/CrabInHoney/urlbert-tiny-v4-phishing-classifier
# I am not the original creator of the following code

from transformers import BertTokenizerFast, BertForSequenceClassification, pipeline
import torch

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Используемое устройство: {device}")

model_name = "CrabInHoney/urlbert-tiny-v4-phishing-classifier"

tokenizer = BertTokenizerFast.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name)
model.to(device)

classifier = pipeline(
    "text-classification",
    model=model,
    tokenizer=tokenizer,
    device=0 if torch.cuda.is_available() else -1,
    return_all_scores=True
)

test_urls = [
    "huggingface.co/",
    "hu991ngface.com.ru/"
]

label_mapping = {"LABEL_0": "good", "LABEL_1": "fish"}

for url in test_urls:
    results = classifier(url)
    print(f"\nURL: {url}")
    for result in results[0]: 
        label = result['label']
        score = result['score']
        friendly_label = label_mapping.get(label, label)
        print(f"Класс: {friendly_label}, вероятность: {score:.4f}")
