import pandas as pd
from pprint import pprint
import random
import aamoshdahal
import crabInHoney
import cybersectony
import ealvardob
from tqdm import tqdm
from urlextract import URLExtract

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
    email_list = loadEmails("TestingDataset.csv")
    random_email = random.choice(email_list)
    
    # email being tested
    print("Testing the models on the following phishing email:")
    print(f"Subject: {random_email["subject"]}")
    print("Body:")
    print(random_email["body"])

    # outputs aamoshdahal
    print("\naamoshdahal outputs:")
    body_outputs_1 = aamoshdahal.predict(random_email["body"])
    pprint(body_outputs_1)

    # outputs ealvardob
    print("\n\nealvardob outputs:")
    body_outputs_2 = ealvardob.predict(random_email["body"])
    pprint(body_outputs_2)

    # outputs crabInHoney
    print("\n\ncrabInHoney outputs:")

    extractor = URLExtract()
    urls = extractor.find_urls(random_email["body"])

    url_outputs = None
    # only run if there are url(s)
    if urls and len(urls) > 0:
        url_outputs = crabInHoney.predict_url(urls)
        pprint(url_outputs)
    else:
        print("No URLs to examine")

    # outputs cybersectony
    print("\n\ncybersectony outputs:")
    url_body_outputs = cybersectony.predict(random_email["body"])
    pprint(url_body_outputs)


if __name__ == "__main__":
    main()