# blood donation chatbot
This is a chatbot app for answering questions on the domain of blood donation. It uses a dynamic few-shot prompting technique, retrieving the best matching samples from a vetor database containing FAQ extracted from [American Red Cross](https://www.redcrossblood.org/faq.html)

## Dependencies
* Install all required dependencies from `requirements.txt` with a dependency manager or your choice
* Or, if using pipenv, just run ```pipenv install``` inside the project folder


## Run the app 

To run the app enter the following command:
```console
$ streamlit run gui.py
```

## Run on command line
To run the chatbot feature on the command line execute the `bot.py` script:
```console
$ python bot.py
```

To add new samples to the database run the `add_data.py` script and pass a json file as argument containing the samples (see example below):
```console
$ python add_data.py <path_json_file>
```
JSON file: 
```json
{
    "data": [
        {
            "question": "question (str)",
            "answer": "answer (str)",
            "category": "category (str | null)"
        },
        {
            "question": "question (str)",
            "answer": "answer (str)",
            "category": "category (str | null)"
        }
    ]
}
```

## Examples
Here are some examples of questions you might ask:
1. What should I expect during the blood donation appointment?
2. What are the eligibility criteria for donating blood?
3. How much time should I wait between donations?
4. Why is it important to have a diverse blood donor base?
5. Can I donate blood if I’m taking medication or have a medical condition?
6. How should I take care of myself before and after donating blood?  
7. How does blood donation affect my daily activities or exercise routine?
8. How long does it take to donate blood, including registration and recovery?
9. Am I able to donate blood if I have a tattoo?
10. How does my weight and height affect the donation?


