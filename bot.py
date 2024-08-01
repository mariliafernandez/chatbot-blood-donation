from src.Chat import Chat

if __name__ == "__main__":
    chat = Chat()
    question = input("\nEnter your question or 0 to exit: ")
    while question != '0':
        answer, samples = chat.ask(question)
        print(answer)
        print("----------------\nRelated samples")
        print(samples)
        question = input("\nEnter your question: ")
