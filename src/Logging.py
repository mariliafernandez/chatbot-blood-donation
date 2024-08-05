from typing import List
from pathlib import Path
from datetime import datetime
import json


class Logging:
    def __init__(self, output_dir: str) -> None:
        self.dir = Path(output_dir)
        self.dir.mkdir(exist_ok=True, parents=True)
        self.created = datetime.now()
        self.records = []

    def add(self, question: str, retrieved: List[str], answer: str):
        obj = {
            "question": question,
            "retrieved": retrieved,
            "answer": answer,
            "timestamp": datetime.now().isoformat(),
        }
        self.records.append(obj)

    def write(self):
        filename = self.created.strftime("%Y%m%d-%H%M%S")
        filepath = self.dir / f"{filename}.json"

        obj = {
            "created_at": self.created.isoformat(),
            "finished_at": datetime.now().isoformat(),
            "data": self.records,
        }

        with open(filepath, "w", encoding="utf-8") as fp:
            json.dump(obj, fp, indent=4)

        print("saved logfile:", filepath)

    def add_and_write(self, question: str, retrieved: List[str], answer: str):
        self.add(question, retrieved, answer)
        self.write()