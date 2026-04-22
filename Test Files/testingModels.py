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
from letsGoPhishing import getUrls

# Load the models, a print added for visuals
import gptMini
import aamoshdahal
import crabInHoney
import cybersectony
import ealvaradob

MODEL = "crabInHoney"

def main():
    print()
    email_list = loadEmails("TestingDataset.csv")
    print()
    email_range = 100
    start_range = 0
    filename = f"modelTest_{MODEL}_{email_range}_1.txt"

    with open(filename, 'a') as file:
        file.write(f"Test results based off {email_range} emails starting from email {start_range + 1}\n\n")

    # counts for system
    num_guesses = 0
    num_right = 0
    num_false_negative = 0
    num_false_positive = 0

    num_dis = 0

    # tests for model
    for i in range(start_range, start_range + email_range):
        check_results = runModel(email_list[i])
        votes = check_results[0]
        num_guesses += 1
        
        if isinstance(votes, int):
            vote = votes
        else:
            vote = votes[0]

        # checking the system to the actual
        print(f"Score: {vote}. Email Score: {check_results[1]}")
        with open(filename, 'a') as file:
            file.write(f"Score: {vote}. Email Score: {check_results[1]}\n")

        if vote == check_results[1]:
            # correct guess
            num_right += 1
        elif vote == 0:
            # guessed no scam but it was
            num_false_negative += 1
        else:
            # guessed scam but it was not
            num_false_positive += 1

    # percents
    percent_correct = num_right / num_guesses
    percent_fp = num_false_positive / num_guesses
    percent_fn = num_false_negative / num_guesses

    print(f"\n=== RESULTS ===\nPercent guessed right: {percent_correct}\nPercent false positive: {percent_fp}\nPercent false negative: {percent_fn}")

    with open(filename, 'a') as file:
        file.write(f"\n=== RESULTS ===\nPercent guessed right: {percent_correct}\nPercent false positive: {percent_fp}\nPercent false negative: {percent_fn}")

def runModel(email):
    # change this line to change the type of model used, comment out if using crabInHoney
    # model_outputs = ealvaradob.predict(email["body"])

    # uncomment this when using crabInHoney
    model_outputs = getUrls(email)

    output = 0
    if model_outputs:
        if "legitimate" not in model_outputs["pred"]:
            output = 1

    return output, email["label"]

if __name__ == "__main__":
    main()