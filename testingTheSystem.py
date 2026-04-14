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
    filename = "systemTest_disagreement labels_100_1"
    email_range = 100
    start_range = 10000

    with open(filename, 'a') as file:
        file.write(f"Test results based off {email_range} emails starting from email #{start_range + 1}\n\n")

    # counts for system
    num_guesses = 0
    num_right = 0
    num_false_negative = 0
    num_false_positive = 0

    num_dis = 0

    for i in range(start_range, start_range + email_range):
        check_results = runCheck(email_list[i])
        dis_scores = check_results[4]
        models = check_results[5]

        num_guesses += 1

        if dis_scores[1] > 0:
            num_dis += 1
            print(f"Disagreement found")
            for model in models:
                print(f"Label: {model["pred"]}")
            with open(filename, 'a') as file:
                file.write(f"Disagreement found\n")
            print()
        else:
            print(f"Agreed")
            with open(filename, 'a') as file:
                file.write(f"Agreed\n")

    print(f"\n=== RESULTS ===\nAmount disagreed: {num_dis}\nNumber agreed: {num_guesses-num_dis}\nPercent disagreed: {(num_dis)/(num_guesses-num_dis)}")

    with open(filename, 'a') as file:
        file.write(f"\n=== RESULTS ===\nAmount disagreed: {num_dis}\nNumber agreed: {num_guesses-num_dis}\nPercent disagreed: {(num_dis)/(num_guesses-num_dis)}")

    # tests for aamoshdahal
    # for i in range(start_range, email_range):
    #     # chosen_email = random.choice(email_list)
    #     check_results = runAamoshdahal(email_list[i])
    #     num_guesses += 1
        
    #     # checking the system to the actual
    #     print(f"Score: {check_results[0]}. Email Score: {check_results[1]}")
    #     with open(filename, 'a') as file:
    #         file.write(f"Score: {check_results[0]}. Email Score: {check_results[1]}\n")

    #     if check_results[0] == check_results[1]:
    #         # correct guess
    #         num_right += 1
    #     elif check_results[0] == 0:
    #         # guessed no scam but it was
    #         num_false_negative += 1
    #     else:
    #         # guessed scam but it was not
    #         num_false_positive += 1


    # tests for chosen email
    # for i in range(start_range, email_range):
    #     # chosen_email = random.choice(email_list)
    #     check_results = runCheck(email_list[i])
    #     num_guesses += 1
        
    #     # checking the system to the actual
    #     print(f"Score: {check_results[1]}. Scam Point: {check_results[2]}. Email Score: {check_results[3]}")
    #     with open(filename, 'a') as file:
    #         file.write(f"Score: {check_results[1]}. Scam Point: {check_results[2]}. Email Score: {check_results[3]}\n")

    #     if check_results[2] == check_results[3]:
    #         # correct guess
    #         num_right += 1
    #     elif check_results[2] == 0:
    #         # guessed no scam but it was
    #         num_false_negative += 1
    #     else:
    #         # guessed scam but it was not
    #         num_false_positive += 1

    # percents
    # percent_correct = num_right / num_guesses
    # percent_fp = num_false_positive / num_guesses
    # percent_fn = num_false_negative / num_guesses

    # print(f"\n=== RESULTS ===\nPercent guessed right: {percent_correct}\nPercent false positive: {percent_fp}\nPercent false negative: {percent_fn}")

    # with open(filename, 'a') as file:
    #     file.write(f"\n=== RESULTS ===\nPercent guessed right: {percent_correct}\nPercent false positive: {percent_fp}\nPercent false negative: {percent_fn}")

def runAamoshdahal(email):
    model_outputs = cybersectony.predict(email["body"])

    output = 1
    if "legitimate" in model_outputs["pred"]:
        output = 0

    return output, email["label"]

if __name__ == "__main__":
    main()