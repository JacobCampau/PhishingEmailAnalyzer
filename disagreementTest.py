import pandas as pd
from pprint import pprint
import random
from tqdm import tqdm
from urlextract import URLExtract
import re
import os

# Load my local environment variables for tokens
from dotenv import load_dotenv
load_dotenv()

# functions needed from the main file in letsGoPhishing
from letsGoPhishing import loadEmails
from letsGoPhishing import findDisagreement

# Load the models, a print added for visuals
import gptMini
import aamoshdahal
import crabInHoney
import cybersectony
import ealvaradob

def main():
    print()
    email_list = loadEmails("TestingDataset.csv")
    print()
    email_range = 100
    start_range = 0
    filename = f"disagreementTest_{email_range}_1.txt"

    with open(filename, 'a') as file:
        file.write(f"Test results based off {email_range} emails starting from email {start_range + 1}\n\n")

    # counts for system
    num_guesses = 0
    num_dis = 0

    for i in range(start_range, start_range + email_range):
        email = email_list[i]

        body_outputs_1 = aamoshdahal.predict(email["body"])
        body_outputs_2 = ealvaradob.predict(email["body"])
        url_body_outputs = cybersectony.predict(email["body"])

        extractor = URLExtract()
        urls = extractor.find_urls(email["body"])

        url_outputs = None
        # only run if there are url(s)
        if urls and len(urls) > 0:
            all_url_outputs = []
            phishing_urls = []

            for url in urls:
                url_result = crabInHoney.predict_url(url)
                all_url_outputs.append(url_result)
                if url_result["pred"] == "phishing":
                    phishing_urls.append(url_result)

            # if there are phishing urls, choose the url result with the highest phishing confidence
            if phishing_urls:
                url_outputs = max(phishing_urls, key=lambda x: x["confidence"])
            else:
                url_outputs = max(all_url_outputs, key=lambda x: x["confidence"])

        # disagreement detection
        model_array = [body_outputs_1, body_outputs_2, url_body_outputs]
        if urls and len(urls) > 0:
            # add the url stuff if there are urls
            model_array.append(url_outputs)
            
        disagreement_scores = findDisagreement(model_array)

        num_guesses += 1

        if disagreement_scores[1] > 0:
            num_dis += 1
            print(f"Disagreement found")
            for model in model_array:
                print(f"Label: {model["pred"]}")
            with open(filename, 'a') as file:
                file.write(f"Disagreement found\n")
            print()
        else:
            print(f"Agreed")
            with open(filename, 'a') as file:
                file.write(f"Agreed\n")

    print(f"\n=== RESULTS ===\nAmount disagreed: {num_dis}\nNumber agreed: {num_guesses-num_dis}\nPercent disagreed: {(num_dis)/(num_guesses)}")

    with open(filename, 'a') as file:
        file.write(f"\n=== RESULTS ===\nAmount disagreed: {num_dis}\nNumber agreed: {num_guesses-num_dis}\nPercent disagreed: {(num_dis)/(num_guesses)}")

if __name__ == "__main__":
    main()