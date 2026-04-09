import pandas as pd
from pprint import pprint
import random
from tqdm import tqdm
from urlextract import URLExtract

# Load my local environment variables for tokens
from dotenv import load_dotenv
load_dotenv()

# Load the models, a print added for visuals
print("Loading models...")
import gptMini
import aamoshdahal
import crabInHoney
import cybersectony
import ealvaradob

def main():
    print("Let's Go Phishing Main Page\nLoading Emails...")
    email_list = loadEmails("TestingDataset.csv")
    chosen_email = random.choice(emails)

    # counts
    num_guesses = 0
    num_right = 0
    num_false_negative = 0
    num_false_positive = 0
    
    # tests
    for _ in range(5):
        check_results = runCheck(chosen_email)
        num_guesses += 1
        
        print(f"Score: {check_results[1]}. Scam Point: {check_results[2]}. Email Score: {check_results[3]}")
        
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

    print(f"\n=== RESULTS ===\nPercent guessed right: {percent_correct}\nPercent false positive: {percent_fp}\nPercent false negative: {percent_fn}\n")


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

def runCheck(email):
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
    confidence_array = [body_outputs_1, body_outputs_2, url_body_outputs]
    if urls and len(urls) > 0:
        # add the url stuff if there are urls
        confidence_array.append(url_outputs)
        
    disagreement_scores = findDisagreement(confidence_array)

    # get gpt response and analysis
    scam_results = getAnalysis(email["body"], disagreement_scores, body_outputs_1, body_outputs_2, url_outputs, url_body_outputs)
    scam_point = None

    if scam_results[1] > 0.6:
        # no scam
        scam_point = 1
    elif scam_results[1] < 0.4:
        # it's a scam
        scam_point = 0
    else:
        # an uncertain score will just say it's a scam to be safe
        scam_point = 1

    return scam_results[0], scam_results[1], scam_point, email["label"], disagreement_scores

def getAnalysis(email, dis_scores, b_output_1, b_output_2, u_output, b_u_output):
    response = None

    if dis_scores[0] > 0 or dis_scores[1] > 0:
        # there was a disagreement
        # disagreement analysis with gpt
        dis_prompt = f"""
        There has been a disagreement between four language models while reading through this email while trying to detect a phishing scam. In the following email contained within quotation marks: 
        
        "{email}"
        
        The first model is an email body analyzer called aamoshdahal and gave the following results: {b_output_1}
        The second model is an email body analyzer called ealvaradob and gave the following results: {b_output_2}
        The third model is an url analyzer called crabInHoney and gave the following results: {u_output}
        The fourth model is an email body and url analyzer and gave the following results: {b_u_output}
        
        From these models, {dis_scores[0]} of them disagreed based on a 10% confidence disagreement and {dis_scores[1]} of them disagreed based on their pred label.
        
        Using specific reasons from the email being analyzed in this prompt, give me an explination for why this disagreement has occured. 
        
        Keep the response minimal while giving a detailed explination that a high schooler could understand. Minimal header and indentation. The answer should be structured with these categories: "Body analysis differences", "URL analysis differences", and a final "Overall" section. Do not add any '#' or '*' to the headers. Refer to the models by their name.
        
        Finally, on its own line, give your own prediction on how likely the email is a scam, based on the model outputs and the analysis you just gave of their disagreements, by printing a number between 0 and 1 where 0 is not a scam and 1 is a scam. Only print the number, not explination or sentence following it.
        """

        response = gptMini.get_analysis(dis_prompt)
    else:
        # there was no disagreement
        # using gpt to get a value based on the model outputs
        agree_prompt = f"""
        Using this email contained within quotation marks: "{email}" I passed this email through four phishing scam analyzers
        The first is aamoshdahal, which looked at the email body and had the results {b_output_1}
        The second was ealvaradob, which looked at the email body and had the results {b_output_2}
        The third was crabInHoney, which looked at the urls in the email had the results {u_output}
        The fourth was cybersectony, which looked at the urls and email body had the results {b_u_output}

        For your response, on its own line, give your own prediction on how likely the email is a scam, based on the model outputs, by printing a number between 0 and 1 where 0 is not a scam and 1 is a scam. Only print the number, not explination or sentence following it.
        """

        response = gptMini.get_analysis(agree_prompt)

    # scraping the final conclusion value from the analysis prediction.
    gpt_prediction = float(response.strip().split()[-1])

    return response, gpt_prediction

def findDisagreement(confidence_array):
    confidence_score = 0
    label_score = 0
    
    for i in range(len(confidence_array)):
        model_1 = confidence_array[i]
        label_disagreement = False
        confidence_disagreement = False

        for j in range(i+1, len(confidence_array)):
            if i == j:
                continue

            model_2 = confidence_array[j]

            # Early check
            if confidence_disagreement and label_disagreement:
                break

            # Confidence Check
            if not confidence_disagreement:
                if abs(model_1["confidence"] - model_2["confidence"]) > 0.1:
                    confidence_disagreement = True

            # Label Check
            if not label_disagreement:
                if "cybersectony" in model_1["model_id"]:
                    match = model_2["pred"] in model_1["pred"]
                elif "cybersectony" in model_2["model_id"]:
                    match = model_1["pred"] in model_2["pred"]
                else:
                    match = model_1["pred"] == model_2["pred"]

                if not match:
                    label_disagreement = True
        
        if confidence_disagreement:
            confidence_score += 1
        if label_disagreement:
            label_score += 1

    return confidence_score, label_score

if __name__ == "__main__":
    main()