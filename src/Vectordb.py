from chromadb import Collection, PersistentClient
from typing import Dict, List
import json
from uuid import uuid4


class Vectordb:
    def __init__(self) -> None:
        self.client = PersistentClient(path="./chromadb")
        self.collection = self.get_or_create_collection("faq_redcross")

    def get_or_create_collection(self, collection_name: str) -> Collection:
        if collection_name in [c.name for c in self.client.list_collections()]:
            return self.client.get_collection(collection_name)
        return self.create_and_populate_collection(collection_name)

    def create_and_populate_collection(self, collection_name: str) -> Collection:
        collection = self.client.create_collection(name=collection_name)
        with open("data/faq.json", "r", encoding="utf-8") as fp:
            data = json.load(fp)
        self.add_faq_records(data["faqs"])
        return collection

    def add_faq_records(self, faq_records: List[Dict]) -> None:
        documents = [self._build_faq_string(item) for item in faq_records]
        self.collection.add(
            documents=documents, ids=[str(uuid4()) for _ in range(len(documents))]
        )
        print(
            f"Added {len(documents)} records, collection {self.collection.name} has now {self.collection.count()} records."
        )

    def retrieve(self, query: str, n: int = 3) -> List[str]:
        results = self.collection.query(
            query_texts=[query], n_results=n, include=["documents"]
        )
        return results["documents"][0]

    def _build_faq_string(self, faq_record: Dict) -> str:
        if faq_record["category"] != None and (faq_record["category"]).strip() != "":
            return f"Category: {faq_record['category']} \n\nQ: {faq_record['title']} \n\nA: {faq_record['description']}"
        return f"Q: {faq_record['title']} \n\nA: {faq_record['description']}"
