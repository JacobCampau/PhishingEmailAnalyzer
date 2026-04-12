<h2>Logs</h2>
This text document will detail my progress over time with this project.

<h3>02/19/2026</h3>
This is the first day working on this project, so it will be spent adding files and starting to look for potential models.

<br>Added the default code from 5 phishing models found on hugging face. Of them, 4 provided easy setup code. May need to look elsewhere for more models if these turn out to not be very unique in their outputs or reliability scores found during testing.

<h3>02/24/2026</h3>
Second day working on this and I have started to make a testing python file. This file will fill a list with a csv found from kaggle. Then using the models I have found, will pass the email body/subject/url into the desired model for testing. Each model's output will be printed and I will be able to see how the different models output their data/results.

<br>Once I have this figured out more, I will change the code to test the results based on the kaggle answers in the csv.

<h3>03/10/2026</h3>
Today I worked on and made the crabInHoney file work. It is now able to take in the URL from an email body and give its outputs in the same format as with the first model. The last three models should be much faster now that I can see the patterns in how these models are used from hugging face. In fact, I wouldn't be surprised if I have to redo some of it to match the lecture collab notebooks better. 

<h3>03/11/2026</h3>
Had to rework the project. Where originally this project would describe phishing scams better, it is now going to analyze disagreements between models. This should help identify the areas in which current phishing models still struggle. So the new method will use two body models, one url model, and one model that does url and body analysis. Then based on the outputs, I will find if any disagreements have occured. If a disagreemnt occurs, it will use a gpt mini model to explain the issue. Last minute pivot that should be innovative for this project.

<h3>03/22/2026</h3>
Made a working disagreement system. If the four models disagree, it will be found based on this criteria: Either one or more models differ in confidence by more than 10% OR at least one model has a different label output than the rest. This should allow me to then pass the outputs, labels, confidence levels, prodabilities in each label, and the disagreement counts for how many models disagree into a gpt model that will then give an easy to read output for the users.

<br>It was brought to my attention during my pitch that while this tool can help users, it can also help scammers get better at attacks. My counter to that would be that these tools are already available to scammers. If they wanted to test their scams to be better, they could do it easily. If I can make this system in a few weeks, a scammer could make a much better tool within a few months. The idea is to help users keep up with the tools available to scammers.

<h3>03/31/2026</h3>
Added the gpt4 mini model to the system. Found out I need to keep a balance on the account, so I will need to monitor that. So far i have loaded it with $5, but it will certainly affect how my prompt is set up. So far have not tested it, but I will soon. If all goes well, this should be the near end of the coding before I begin work on the UI.

<br>I was able to get the chat gpt explination working. The response seems very generic, and I was hoping for a specific analysis on the email given. The response was also much longer than I had wanted. As such, I will need to tweak the prompt to make the response both simpler and more specific to the email being analyzed.

<br>Before beginning to tweak the prompt too much, I want to fix another issue. Every time this system runs, it has to load the models seperatly and save them to the cache. This process always takes a long time. As such, to speed up the loading times, I am going to make a python script to download these models locally. Then in each of their folders, I will change them so they pull the models from the locally saved files, rather than the hugging face website. Ideally this should speed up the process so the system is actually usable for users.

<br>I was able to tweak the prompt being sent to the gpt model such that it will give a paragraph on the body analysis disagreements, a paragraph for url disagreements, and a final overall paragraph. I also made the models all be saved locally. Overall, the project now runs faster and gives an output I was hoping to obtain. Now I need to design the UI and continue tweaking the prompt so it will give the type of analysis I want the user to be able to see.

<h3>04/09/2026</h3>
Separated the main function into multiple functions to help with modularity and reading clarity. Also made a new python script for testing my system compared to the other models. Currently setup to run and give a percent of answers that were correct, the percent of false positives, and the percent of false negatives with respect to the combined system. Now I need to setup a section in the same file to test the other models individually for a comparison. They should be tested on the same emails to ensure the comparison is fair. 

<h3>04/11/2026</h3>
Ran the first tests for the system. On a sample of 500 emails it performed with 65% correct answers, way under performing. It also had 11% false negatives and 24% false positives when guessing an email was a scam. This is not good. I need to reign in the prompt engineering better. May need to redo the prompt completely to get it done. Once I can get this value up, I will test the other models and make a simple UI. Will likely need to stick to a CLI so I dont need to waste too much time on that and can focus on making the system more accurate.

<h3>04/11/2026</h3>
Changing the prompts to be more concise. Looking back on them, I am still treating the gpt model as a human with the way I am giving it directions. For example, the original aggreement response looked like this:

    f"""
    Using this email contained within quotation marks: "{email}" I passed this email through four phishing scam analyzers
    The first is aamoshdahal, which looked at the email body and had the results {b_output_1}
    The second was ealvaradob, which looked at the email body and had the results {b_output_2}
    The third was crabInHoney, which looked at the urls in the email had the results {u_output}
    The fourth was cybersectony, which looked at the urls and email body had the results {b_u_output}
    
    For your response, on its own line, give your own prediction on how likely the email is a scam, based on the model outputs, by printing a number between 0 and 1 where 0 is not a scam and 1 is a scam. Only print the number, not explination or sentence following it.
    """

<br>It has now been updated to look like:

    f"""
    Using this email and ai model outputs bellow, determine how likely the email is a phishing scam
    
    Email: \"{email_body}\"
    
    Model Outputs:
    - aamoshdahal (body analysis): {model_array[0]}
    - ealvardob (body analysis): {model_array[1]}
    - cybersectony (body and url analysis): {model_array[2]}
    - crabInHoney (url analysis): {url_results}
    
    Output exactly 1 line.
    That line must be a number between 0 and 1.
    It should reflect the probability this email is a scam (0 is no scam, 1 is a scam).
    The probability must be based on and agree with, the model outputs.
    """

<br>And it has been placed in its own function to help simplify the look of the getAnalysis function. The disagreement analysis was most important and changed from this:

    f"""
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

<br>To this:

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

<br>On running these new prompts for 10 emails, the results seemed to be worse. But I believe it will open up the system to produce a better set of disagreement analysis. I believe this project would better be set as a way to find where disagreement models are lacking rather than trying to make a better one by combining multipl models. I will show this pivot in my final report and demo. I will define a new function for saving disagreements to a separate file so they can be further analyzed at the end of this project.
