from Chat import Chat

if __name__ == "__main__":
    chat = Chat()
    question = None
    while question != '0':
        question = input("Enter your question or 0 to exit: ")
        samples = chat._get_related_samples(question)
        prompt = chat._build_prompt(samples)
        print(prompt)