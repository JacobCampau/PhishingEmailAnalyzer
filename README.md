<h1>Phishing Email Analyzer</h1>
<h2>Project Goals</h2>

The overall plan for the project can be explained in the following steps:

  1. Get a list of different Hugging Face LLMs designed to identify phishing scams<br>
  2. Make a custom dataset to test each of the models with<br>
    - Need to find out what kind of outputs the models give, and determine which to use in the project<br>    
  3. Design an automated test for each model<br>
    - For the models that have overlapping outputs, compare the outputs and determine which models are best suited for each output<br>
     (i.e. if multiple models have an output detailing urgency indicators in the email, which model produces the most accurate results?)   
  4. Program a python script that deoes the following:<br>
    - Take in user input for email details and the email body<br>
    - Pass the email through each model to get each individual output from all models used<br>
    - Based on my results from the third step, select the parts of each output I want<br>
    - Store these outputs to get a list of attributes that I can then use to train my own transformer model<br>
  5. Train my own transformer model<br>
    - Using 1 to 3 transformers, train a new model on a separate custom dataset that will output a 0 to 1 score based on the other model's outputs<br>

The goal of this project is to learn how to train a custom small LLM and understand different ways models can generate outputs. The project itself will be used as my CS 491 LLM class final.

<h2>Project Results</h2>

The end system architecture looks as the following
<img src="https://imgur.com/LGSwmPH" height="80%" width="80%" alt="Flow Chart"/>

The original plan was to train a mini transformer model using the kaggle dataset I found. However, this plan changed shortly after starting this project. Due to the short timeframe I determined this may take too long. So I pivoted to develop a chat gpt explination model. 

<br>The new model reads in the email and pass it through all the different models. After getting the outputs, it determines if any disagreed based on their level of confidence or their prediction labels. Depending on if there is a disagreement or not, either an agreement prompt or disagreement prompt will be made. This prompt is then passed through a majority vote function. This function passes the prompt to a gpt 4 mini model and gets a value of whether the email is a scam based on the model outputs 3 plus times. The average value is then taken and is passed back to the main function as the scam score where 1 is scam and 0 is no scam.</br>

<br>The final result of this system was not as expected. The system did not perform more accurately than the individual models. However, it did produce 1% less false "not a scam" results than the individual models. Overall, the final results from each model versus the system is as follows.</br>
        
    === System ===
    - Accuracy: 73%
    - False Negative: 20%
    
    === Model by Aamoshdahal ===
    - Accuracy: 79%
    - False Negative: 21%

    === Model by Ealvardob ===
    - Accuracy: 76%
    - False Negative: 21%
    
    === Model by CrabInHoney ===
    - Accuracy: 50%
    - False Negative: 31%

    === Model by Cybersectony ===
    - Accuracy: 75%
    - False Negative: 21%

    === Disagreement Results ===
    - Percent of Time Disagreements Arrise: 59%

<br>Where this project stands, there is still much room for improvement. The voting system could be made to be faster and include more votes. The prompt engineering can also have some work. By including the voting system, the accuracy increase from 65.4% to 73%. And before that, improving the disagreement and agreement prompts also improved accuracy. Overall, this project would work better if it ran the models across a wide range of emails and made one analysis of what parts of the emails commonly caused disagreements. This would help inform developers for what new phishing models should look for, improving consumer security for all.</br>
