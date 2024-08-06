from chromadb import Collection, PersistentClient
from typing import Dict, List
import json
from uuid import uuid4


class MissingField(Exception):
    pass


class Vectordb:
    def __init__(self, name: str) -> None:
        self.name = name
        self.client = PersistentClient(path="./chromadb")
        self.get_or_create_collection(name)

    def get_or_create_collection(self, collection_name: str) -> Collection:
        """Returns a collection named collection_name if it exists. Otherwise, creates and populates the collection"""
        if collection_name in [c.name for c in self.client.list_collections()]:
            self.collection = self.client.get_collection(collection_name)
        else:
            self.create_and_populate_collection(collection_name)

    def create_and_populate_collection(self, collection_name: str) -> Collection:
        """Created a new collection and populates it with initial data"""
        self.collection = self.client.create_collection(name=collection_name)
        with open(f"data/{self.name}.json", "r", encoding="utf-8") as fp:
            data = json.load(fp)
        self.add_faq_records(data["data"])
        return self.collection

    def validate_fields(self, faq_record: Dict) -> bool:
        required_fields = ["question", "answer"]
        return all([required in faq_record.keys() for required in required_fields])

    def add_faq_records(self, faq_records: List[Dict]) -> None:
        """Adds a new FAQ record to database"""
        if not all([self.validate_fields(record) for record in faq_records]):
            raise MissingField

        documents = [self._build_faq_string(item) for item in faq_records]
        self.collection.add(
            documents=documents, ids=[str(uuid4()) for _ in range(len(documents))]
        )
        print(
            f"Added {len(documents)} records, collection {self.collection.name} has now {self.collection.count()} records."
        )

    def retrieve(self, query: str, n: int = 3) -> List[str]:
        """Returns the n records most related to the query"""
        results = self.collection.query(
            query_texts=[query], n_results=n, include=["documents"]
        )
        return results["documents"][0]

    def _build_faq_string(self, faq_record: Dict) -> str:
        """Returns a string representing the faq_record"""
        if (
            "category" in faq_record
            and faq_record["category"] != None
            and (faq_record["category"]).strip() != ""
        ):
            return f"Category: {faq_record['category']} \n\nQ: {faq_record['question']} \n\nA: {faq_record['answer']}"
        return f"Q: {faq_record['question']} \n\nA: {faq_record['answer']}"
