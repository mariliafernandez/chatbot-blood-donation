from src.Chat import Chat
from src.Vectordb import MissingField
from pathlib import Path
import sys
import json


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Missing json_path argument")
    else:
        json_path = Path(sys.argv[1])
        if json_path.exists():
            with open(json_path, "r", encoding="utf-8") as fp:
                data = json.load(fp)
            chat = Chat("redcross")
            try:
                chat.vectordb.add_faq_records(data['data'])
            except MissingField:
                print("Invalid input data: Missing required fields.\nCheck readme.md for instructions.")
        else:
            print(f"{json_path} does not exist")