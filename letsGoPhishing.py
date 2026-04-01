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

    # email being tested
    print("Testing the models on the following phishing email:")
    # print(f"Subject: {random_email["subject"]}")
    print("Subject: CNN.com Daily Top 10")
    print("Body:")
    # print(random_email["body"])
    print(chosen_email)

    # outputs aamoshdahal
    print("\n\naamoshdahal outputs:")
    body_outputs_1 = aamoshdahal.predict(chosen_email)
    print(f"Prediction: {body_outputs_1["pred"]}. Confidence is: {body_outputs_1["confidence"]}")
    # pprint(body_outputs_1)

    # outputs ealvardob
    print("\nealvardob outputs:")
    body_outputs_2 = ealvaradob.predict(chosen_email)
    print(f"Prediction: {body_outputs_2["pred"]}. Confidence is: {body_outputs_2["confidence"]}")
    # pprint(body_outputs_2)

    # outputs crabInHoney
    print("\ncrabInHoney outputs:")

    extractor = URLExtract()
    urls = extractor.find_urls(chosen_email)

    url_outputs = None
    # only run if there are url(s)
    if urls and len(urls) > 0:
        url_outputs = crabInHoney.predict_url(urls)
        print(f"Prediction: {url_outputs["pred"]}. Confidence is: {url_outputs["confidence"]}")
        # pprint(url_outputs)
    else:
        print("No URLs to examine")

    # outputs cybersectony
    print("\ncybersectony outputs:")
    url_body_outputs = cybersectony.predict(chosen_email)
    print(f"Prediction: {url_body_outputs["pred"]}. Confidence is: {url_body_outputs["confidence"]}")
    # pprint(url_body_outputs)

    # disagreement detection
    confidence_array = [body_outputs_1, body_outputs_2, url_outputs, url_body_outputs]
    disagreement_scores = findDisagreement(confidence_array)
    if disagreement_scores[0] > 0 or disagreement_scores[1] > 0:
        # there was a disagreement
        print("\n\nDisagreement Found!!\n\n")

        # disagreement analysis with gpt
        dis_prompt = f"""
        There has been a disagreement between four language models while reading through this email while trying to detect a phishing scam. In the following email contained within quotation marks: 
        
        "{chosen_email}"
        
        The first model is an email body analyzer called aamoshdahal and gave the following results: {body_outputs_1}
        The second model is an email body analyzer called ealvaradob and gave the following results: {body_outputs_2}
        The third model is an url analyzer called crabInHoney and gave the following results: {url_outputs}
        The fourth model is an email body and url analyzer and gave the following results: {url_body_outputs}
        
        From these models, {disagreement_scores[0]} of them disagreed based on a 10% confidence disagreement and {disagreement_scores[1]} of them disagreed based on their pred label.
        
        Using specific reasons from the email being analyzed in this prompt, give me an explination for why this disagreement has occured. 
        
        Keep the response minimal while giving a detailed explination that a high schooler could understand. Minimal header and indentation. The answer should be structured with these categories: "Body analysis differences", "URL analysis differences", and a final "Overall" section. Do not add any '#' or '*' to the headers. Refer to the models by their name.
        
        Finally, on its own line, give your own prediction on how likely the email is a scam, based on the model outputs and the analysis you just gave of their disagreements, by printing a number between 0 and 1 where 0 is not a scam and 1 is a scam. Only print the number, not explination or sentence following it.
        """

        response = gptMini.get_analysis(dis_prompt)

        print("Analysis of disagreement(s):\n")
        print(response)

        # scraping the final conclusion value from the analysis prediction.
        gpt_prediction = float(response.strip().split()[-1])
        if gpt_prediction > 0.6:
            print("\nThis email is likely a scam.")
        elif gpt_prediction < 0.4:
            print("\nThis email is likely not a scam")
        else:
            print("\nIt is hard to say for sure if this email is a scam. Proceed with caution.")
    else:
        # there was no disagreement
        print("\n\nNo disagreement found\n\n")

        # using gpt to get a value based on the model outputs
        agree_prompt = f"""
        Using this email contained within quotation marks: "{chosen_email}" I passed this email through four phishing scam analyzers
        The first is aamoshdahal, which looked at the email body and had the results {body_outputs_1}
        The second was ealvaradob, which looked at the email body and had the results {body_outputs_2}
        The third was crabInHoney, which looked at the urls in the email had the results {url_outputs}
        The fourth was cybersectony, which looked at the urls and email body had the results {url_body_outputs}
        """


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