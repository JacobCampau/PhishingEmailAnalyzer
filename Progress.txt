This text document will detail my progress over time with this project. The overall goal for the project can be laid out in 2 sections:
  1: Get a list of different Hugging Face LLMs designed to identify phishing scams
  2: Make a custom dataset to test each of the models with
    - Need to find out what kind of outputs the models give, and determine which to use in the project
  3: Design an automated test for each model
    - For the models that have overlapping outputs, compare the outputs and determine which models are best suited for each output
      (i.e. if multiple models have an output detailing urgency indicators in the email, which model produces the most accurate results?)
  4: Program a python script that deoes the following:
    - Take in user input for email details and the email body a
    - Pass the email through each model to get each individual output from all models used
    - Based on my results from the third step, select the parts of each output I want
    - Store these outputs to get a list of attributes that I can then use to train my own transformer model
  5: Train my own transformer model
    - Using 1 to 3 transformers, train a new model on a separate custom dataset that will output a 0 to 1 score based on the other model's outputs

The goal of this project is to learn how to train a custom small LLM and understand different ways models can generate outputs. The project itself will be used as my CS 491 LLM class final.
