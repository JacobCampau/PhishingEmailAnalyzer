import pandas as pd
from pprint import pprint
import random
from tqdm import tqdm
from urlextract import URLExtract
import os


import aamoshdahal
import crabInHoney
import cybersectony
import ealvardob

def loadEmails(filename):
    df = pd.read_csv(filename)
    row_num = len(df)

    emails = []
    chunk_size = 1000

    with tqdm(total=row_num, desc="Importing Emails", unit="Email") as bar:
        for chunk in pd.read_csv(filename, chunksize=chunk_size):
            records = chunk.to_dict(orient="records")
            emails.extend(records)
            bar.update(len(records))
            
    return emails

def main():
    print("Let's Go Phishing Main Page\nLoading Emails...")
    # email_list = loadEmails("TestingDataset.csv")
    # random_email = random.choice(email_list)

    chosen_email = None
    with open("perfect_email.txt", 'r') as file:
        chosen_email = file.read()

    print("Gen Outputs:")
    # email being tested
    print("Testing the models on the following phishing email:")
    # print(f"Subject: {random_email["subject"]}")
    print("Subject: CNN.com Daily Top 10")
    print("Body:")
    # print(random_email["body"])
    print(chosen_email)

    # outputs aamoshdahal
    print("\naamoshdahal outputs:")
    body_outputs_1 = aamoshdahal.predict(chosen_email)
    pprint(body_outputs_1)

    # outputs ealvardob
    print("\n\nealvardob outputs:")
    body_outputs_2 = ealvardob.predict(chosen_email)
    pprint(body_outputs_2)

    # outputs crabInHoney
    print("\n\ncrabInHoney outputs:")

    extractor = URLExtract()
    urls = extractor.find_urls(chosen_email)

    url_outputs = None
    # only run if there are url(s)
    if urls and len(urls) > 0:
        url_outputs = crabInHoney.predict_url(urls)
        pprint(url_outputs)
    else:
        print("No URLs to examine")

    # outputs cybersectony
    print("\n\ncybersectony outputs:")
    url_body_outputs = cybersectony.predict(chosen_email)
    pprint(url_body_outputs)

    # disagreement detection
    confidence_array = [body_outputs_1, body_outputs_2, url_outputs, url_body_outputs]
    disagreement_scores = findDisagreement(confidence_array)
    if disagreement_scores[0] > 0 or disagreement_scores[1] > 0:
        print("\n\nDisagreement Found")

    # Disagreement analysis with gpt
    print("test prompt")
    prompt = f"""
    There has been a disagreement between four language models while reading through this email while trying to detect a phishing scam.
    
    The first model is an email body analyzer called aamoshdahal and gave the following results: {body_outputs_1}
    The second model is an email body analyzer called ealvardob and gave the following results: {body_outputs_2}
    The third model is an url analyzer called crabInHoney and gave the following results: {url_outputs}
    The fourth model is an email body and url analyzer and gave the following results: {url_body_outputs}
    
    From these models, {disagreement_scores[0]} of them disagreed based on a 10% confidence disagreement and {disagreement_scores[1]} of them disagreed based on their pred label.
    
    Using this information, give me an explination for why this disagreement has occured.
    """
    print(prompt)


def findDisagreement(confidence_array):
    confidence_score = 0
    label_score = 0
    
    for i in range(len(confidence_array)):
        for j in range(i+1, len(confidence_array)):
            model_1 = confidence_array[i]
            model_2 = confidence_array[j]

            if abs(model_1["confidence"] - model_2["confidence"]) > 0.1:
                confidence_score += 1

            if "cybersectony" in model_1["model_id"]:
                match = model_2["pred"] in model_1["pred"]
            elif "cybersectony" in model_2["model_id"]:
                match = model_1["pred"] in model_2["pred"]
            else:
                match = model_1["pred"] == model_2["pred"]

            if not match:
                label_score += 1

    return confidence_score, label_score

if __name__ == "__main__":
    main()