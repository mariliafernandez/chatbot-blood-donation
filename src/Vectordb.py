from chromadb import Collection, PersistentClient
from typing import Dict, List
import json
from uuid import uuid4


class Vectordb:
    def __init__(self) -> None:
        self.client = PersistentClient(path="./chromadb")

    def create_collection(self, collection_name: str) -> Collection:
        with open("data/faq.json", "r", encoding="utf-8") as fp:
            data = json.load(fp)
        collection = self.client.create_collection(name=collection_name)
        self.add_faq_records(data["faqs"], collection)
        return collection

    def get_collection(self, collection_name) -> Collection:
        try:
            return self.client.get_collection(name=collection_name)
        except Exception:
            return self.create_collection(collection_name)

    def add_faq_records(
        self,
        faq_records: List[Dict],
        collection: Collection,
    ) -> None:
        documents = [self._build_faq_string(item) for item in faq_records]
        collection.add(
            documents=documents, ids=[str(uuid4()) for _ in range(len(documents))]
        )
        print(
            f"Added {len(documents)} records, collection {collection.name} has now {collection.count()} records."
        )

    def retrieve(self, query: str, collection: Collection, n: int = 3) -> List[str]:
        results = collection.query(
            query_texts=[query], n_results=n, include=["documents"]
        )
        return results["documents"][0]

    def _build_faq_string(self, faq_record: Dict) -> str:
        if faq_record["category"] != None and (faq_record["category"]).strip() != "":
            return f"Category: {faq_record['category']} \n\nQ: {faq_record['title']} \n\nA: {faq_record['description']}"
        return f"Q: {faq_record['title']} \n\nA: {faq_record['description']}"
