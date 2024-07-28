from chromadb import Client, Collection
from typing import Dict, List
import json


class Vectordb:
    def __init__(self) -> None:
        self.client = Client()

    def create_collection(self, collection_name: str) -> Collection:
        with open("data/faq.json", "r", encoding="utf-8") as fp:
            data = json.load(fp)
        collection = self.client.create_collection(name=collection_name)
        self.add_faq_records(collection, data["faqs"])
        return collection

    def get_collection(self, collection_name: str) -> Collection:
        try:
            return self.client.get_collection(name=collection_name)
        except Exception:
            return self.create_collection(collection_name)

    def add_faq_records(self, collection: Collection, faq_records: List[Dict]) -> None:
        documents = [
            f"Category: {item['category']} \n\nQ: {item['title']} \n\nA: {item['description']}"
            for item in faq_records
        ]
        collection.add(
            documents=documents, ids=[f"id_{i}" for i in range(len(documents))]
        )
        print(
            f"Added {len(documents)} records, collection {collection.name} has now {collection.count()} records."
        )

    def retrieve(self, query: str, collection: Collection, n: int = 3) -> List[str]:
        results = collection.query(
            query_texts=[query], n_results=n, include=["documents"]
        )
        return results["documents"][0]
