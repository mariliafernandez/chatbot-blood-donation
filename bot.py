from src.Chat import Chat, EmptyQuestion
from src.Logging import Logging


if __name__ == "__main__":
    chat = Chat("redcross")
    question = input("\nEnter your question or 0 to exit: ")
    log = Logging("logs")

    while question != '0':
        try:
            answer, samples = chat.ask(question)
        except EmptyQuestion as e:
            err_msg = "Question cannot be empty."
            print(err_msg)
        else:
            print("R: ", answer)
            log.add_and_write(question, samples, answer)
        
        question = input("\nEnter your question: ")
