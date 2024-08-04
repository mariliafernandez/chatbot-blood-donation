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
            "title": "question (str)",
            "description": "answer (str)",
            "category": "category (str | null)"
        },
        {
            "title": "question (str)",
            "description": "answer (str)",
            "category": "category (str | null)"
        }
    ]
}
```