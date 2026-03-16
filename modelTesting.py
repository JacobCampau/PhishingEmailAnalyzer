import pandas as pd
from pprint import pprint
import random
#import aamoshdahal
# import crabInHoney
# import elSlay
# import cybersectony
# import ealvardob
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
    print
    email_list = loadEmails("TestingDataset.csv")
    random_email = random.choice(email_list)
    
    # email being tested
    print("Testing the models on the following phishing email:")
    print(f"Subject: {random_email["subject"]}")
    print("Body:")
    print(random_email["body"])

    # outputs aamoshdahal
    # print("\naamoshdahal outputs:")
    # pprint(aamoshdahal.predict(random_email["url"]))

    # outputs crabInHoney
    # print("\ncrabInHoney outputs:")

    # extractor = URLExtract()
    # urls = extractor.find_urls(random_email["body"])

    # pprint(crabInHoney.predict_url(urls))

    # outputs elSlay
    # print("\nelSlay outputs:")
    # pprint(elSlay.predict(random_email["body"]))

    # outputs ealvardob
    # print("\nealvardob outputs:")
    # pprint(ealvardob.predict(random_email["body"]))

    # outputs cybersectony
    # print("\ncybersectony outputs:")
    # pprint(cybersectony.predict(random_email["body"]))
    

if __name__ == "__main__":
    main()