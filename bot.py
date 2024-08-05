from src.Chat import Chat
from src.Logging import Logging


if __name__ == "__main__":
    chat = Chat("redcross")
    question = input("\nEnter your question or 0 to exit: ")
    log = Logging("logs")

    while question != '0':
        try:
            answer, samples = chat.ask(question)
        except Exception as e:
            err_msg = f"Unable to process answer due to the following error: {str(e)}"
            print(err_msg)
            log.add(question, [], err_msg)
        else:
            print("R: ", answer)
            log.add(question, samples, answer)
        
        question = input("\nEnter your question: ")

    log.write()