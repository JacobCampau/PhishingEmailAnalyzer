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
    print("Let's Go Phishing Main Page\n")
    email_list = loadEmails("TestingDataset.csv")
    chosen_email = email_list[2] # this email produced great disagreement scores each time it ran

    # email being tested
    print("Testing the models on the following phishing email:")
    print(f"Subject: {chosen_email["subject"]}")
    print("Body:")
    pprint(chosen_email["body"])

    check_results = runCheck(chosen_email)
    votes = check_results[0]

    if(len(votes)) > 1:
        print("\nModels Disagreed.\nDisagreement Analysis:\n")
        pprint(votes[1])
    else:
        print("\nModels aggreed.")
    print(f"\nFinal determination for chance of scam: {votes[0]}")

# Loading the actual email list
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

### System Functions
def runCheck(email):
    print("\nGetting Model Outputs...")
    body_outputs_1 = aamoshdahal.predict(email["body"])
    body_outputs_2 = ealvaradob.predict(email["body"])
    url_body_outputs = cybersectony.predict(email["body"])
    
    urls = getUrls(email)

    # disagreement detection
    model_array = [body_outputs_1, body_outputs_2, url_body_outputs]
    if urls and len(urls) > 0:
        # add the url stuff if there are urls
        model_array.append(urls)
        
    disagreement_scores = findDisagreement(model_array)

    # get gpt response and analysis
    disagreement_decision = disagreement_scores[0] > 0 or disagreement_scores[1] > 0
    if disagreement_decision:
        # there was a disagreement
        prompt = makeDisagreementPrompt(email, model_array, disagreement_scores)
    else:
        # there was no disagreement
        prompt = makeAgreementPrompt(email, model_array)
    
    final_vote = majorityVote(3, prompt, disagreement_decision)

    return final_vote, email["label"]

def getUrls(email):
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
    
    return url_outputs

def getAnalysis(prompt):
    # get the gpt response
    response = gptMini.get_analysis(prompt)

    # scraping the final conclusion value from the analysis prediction.
    stripped_response = response.strip().split()[-1]

    # try converting final value to float
    try:
        gpt_prediction = float(stripped_response)
    except ValueError:
        gpt_prediction = 0   # default guess it is not a scam
        
    return response, gpt_prediction

def findDisagreement(confidence_array):
    confidence_score = 0
    label_score = 0
    
    print("\nGetting Disagreement Scores...")

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
                if not (model_2["pred"] in model_1["pred"] or model_1["pred"] in model_2["pred"]):
                    label_disagreement = True
        
        if confidence_disagreement:
            confidence_score += 1
        if label_disagreement:
            label_score += 1

    return confidence_score, label_score

### Prompt Creations
def makeDisagreementPrompt(email_body, m_array, d_scores):
    url_results = "No urls were extracted"
    if len(m_array) > 3:
        url_results = m_array[3]
    
    prompt = f"""
    There has been a disagreement between four language models while reading through this email while trying to detect a phishing scam.
    
    Email: \"{email_body}\"
    
    Model Outputs:
    - aamoshdahal (body analysis): {m_array[0]}
    - ealvardob (body analysis): {m_array[1]}
    - cybersectony (body and url analysis): {m_array[2]}
    - crabInHoney (url analysis): {url_results}
    
    Disagreement scores:
    - confidence disagreement count (10% difference in confidence percent): {d_scores[0]}
    - label disagreement count (number of models who disagreed based on their label): {d_scores[1]}

    Using specific reasons from the email and the disagreement score, give an explination for why the disagreement occured. 
    
    Output requirements:
    - No special characters
    - Keep the response concise but still clear and useful
    - Refer to the models by their exact names
    - Do not invent evidence that is not present in the email, model outputs, or disagreement scores
    - Put all explanation before the final line

    On the final line, print a scam probability score on the last line.

    Probability score requirements:
    - Output exactly 1 line.
    - That line must be a number between 0 and 1.
    - It should reflect the probability this email is a scam (0 is no scam, 1 is a scam).
    - The probability must be based on the the model outputs.
    - It must be the last number that appears anywhere in the response.
    - Do not print any words, labels, punctuation, or extra lines after it.
    """

    return prompt

def makeAgreementPrompt(email_body, m_array):
    url_results = "No urls were extracted"
    if len(m_array) > 3:
        url_results = m_array[3]

    prompt = f"""
    Using this email and ai model outputs bellow, determine how likely the email is a phishing scam
    
    Email: \"{email_body}\"

    Model Outputs:
    - aamoshdahal (body analysis): {m_array[0]}
    - ealvardob (body analysis): {m_array[1]}
    - cybersectony (body and url analysis): {m_array[2]}
    - crabInHoney (url analysis): {url_results}

    Output requirements:
    - Output exactly 1 line.
    - That line must be a number between 0 and 1.
    - It should reflect the probability this email is a scam (0 is no scam, 1 is a scam).
    - The probability must be based on and agree with, the model outputs.
    """
    
    return prompt

### GPT Majority Vote
def majorityVote(num_checks, gpt_prompt, dis):
    score_total = 0
    final_score = 0

    print("\nBeginning The Voting...")
    print(f"This will be based off {num_checks} votes")

    response_analysis = []
    for i in range(num_checks):
        print(f"Working on vote number: {i+1}")
        gpt_response = getAnalysis(gpt_prompt)
        response_analysis.append(gpt_response[0])
        score_total += gpt_response[1]

    if score_total/num_checks >= 0.5:
        # at least half agree that the response is a scam, adjust the final score
        final_score = 1
    
    disagree_prompt = f"""
    A check was ran on an email to determine if it was a scam or not {num_checks} times

    Checks (1 through {num_checks} contained within an array):
    - \"{response_analysis}\"
    - At some point in the original testing between 4 model outputs, at least one disagreed and led to these responses

    From these checks, the models agreed the final score should be {final_score} (0 is not a scam, 1 is a scam)

    Give an analysis of where these models most likely disagreed in analyzing the email.
    
    Analysis requirements
    - Keep it simple, no more than 2 paragraphs
    - No fancy headers
    - Must support the final score
    """

    if dis == 1:
        print("Disagreements occured amongst the models, analyzing now...")
        final_response = gptMini.get_analysis(disagree_prompt)
        return final_score, final_response
    return final_score

### Run main on start
if __name__ == "__main__":
    main()
