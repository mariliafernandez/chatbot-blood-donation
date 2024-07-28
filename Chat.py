from typing import List, Dict
from Vectordb import Vectordb

BASE_PROMPT = """You are a helpfull and respectfull assistant who is responsible for answering user questions about BLOOD DONATION. 
Please keep your answers concise and objective. 
If you don't know the answer, DO NOT create one, but suggest the user to get the information in official websites."""


class Chat:
    def __init__(self) -> None:
        self.vectordb = Vectordb()
        self.collection = self.vectordb.get_collection("faq_redcross")

    def ask(self, question: str) -> str:
        # TODO: add LLM to generate answer
        samples = self._get_related_samples(question)
        prompt = self.build_prompt(samples)

    def _get_related_samples(self, question: str) -> List[Dict]:
        return self.vectordb.retrieve(question, self.collection)

    def _build_prompt(self, samples: List[str]) -> str:
        prompt = BASE_PROMPT

        for i, sample in enumerate(samples, start=1):
            prompt += f"\n\n----------------\nEXAMPLE {i}:\n{sample}"

        return prompt
