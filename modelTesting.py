import pandas as pd
import random
from tqdm import tqdm

def loadEmails(filename):
    with open(filename, 'r') as file:
        rowNum = sum(1 for _ in f) - 1 # removed the header

    emails = []
    chunkSize = 1000

    with tqdm(total=rowNum, desc="Importing Emails", unit="Email") as bar:
        for chunk in pd.read_csv(filename, chunksize=chunkSize):
            records = chunk.to_dict(orient="records")
            emails.extend(records)
            bar.update(len(records))
            
    return emails


def main():
    emailList = loadEmails("TestingDataset.csv")
    randomEmail = random.choice(emailList)
    
    print("Testing the models on the following phishing email:")
    print(randomEmail)


if __name__ == "__main__":
    main()