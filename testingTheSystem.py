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
from letsGoPhishing import runCheck
from letsGoPhishing import getAnalysis
from letsGoPhishing import findDisagreement
from letsGoPhishing import makeAgreementPrompt
from letsGoPhishing import makeDisagreementPrompt

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
    filename = "systemTest_10_1"
    email_range = 10
    start_range = 0

    with open(filename, 'a') as file:
            file.write(f"Test results based off {email_range} emails starting from email #{start_range + 1}\n\n")

    # counts for system
    num_guesses = 0
    num_right = 0
    num_false_negative = 0
    num_false_positive = 0

    # tests
    for i in range(start_range, email_range):
        # chosen_email = random.choice(email_list)
        check_results = runCheck(email_list[i])
        num_guesses += 1
        
        # checking the system to the actual
        print(f"Score: {check_results[1]}. Scam Point: {check_results[2]}. Email Score: {check_results[3]}")
        with open(filename, 'a') as file:
            file.write(f"Score: {check_results[1]}. Scam Point: {check_results[2]}. Email Score: {check_results[3]}\n")

        if check_results[2] == check_results[3]:
            # correct guess
            num_right += 1
        elif check_results[2] == 0:
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


if __name__ == "__main__":
    main()