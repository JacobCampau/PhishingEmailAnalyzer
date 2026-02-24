import pandas as pd
from tqdm import tqdm

def loadEmails(filename):
    with open(filename, 'r') as file:
        rowNum = sum(1 for _ in f) - 1 # removed the header

    emails = []
    chunkSize = 1000

    with tqdm(total=rowNum, desc="Importing Emails", unit="Email") as bar:
        def progress(progress, total):
            bar.n = progress
            bar.refresh()


def main():
    print("Testing the models on the following phishing email:")

    email_text = ""

    print(email_text)


if __name__ == "__main__":
    main()