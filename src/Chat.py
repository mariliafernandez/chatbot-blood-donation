from typing import List, Dict
from src.Vectordb import Vectordb
from transformers import pipeline

BASE_PROMPT = """You are a helpfull and respectfull assistant who is responsible for answering user questions about BLOOD DONATION. 
Keep your answers strictly to the subject of BLOOD DONATION and refuse poletely to answer to any other subject.
Please keep your answers concise and objective.
Use the given examples to generate your final answer.
If you don't know the answer, DO NOT create one, but suggest the user to get the information in official websites."""


class Chat:
    def __init__(self) -> None:
        self.vectordb = Vectordb()
        self.collection = self.vectordb.get_collection("faq_redcross")
        self.pipe = pipeline(
            "text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0"
        )

    def ask(self, question: str) -> str:
        samples = self._get_related_samples(question)
        prompt = self._build_prompt(samples)
        result = self.pipe(
            [{"role": "system", "content": prompt}, {"role": "user", "content": question}]
        )
        return result[0]['generated_text'][-1]['content']

    def _get_related_samples(self, question: str) -> List[Dict]:
        return self.vectordb.retrieve(question, self.collection)

    def _build_prompt(self, samples: List[str]) -> str:
        prompt = BASE_PROMPT

        for i, sample in enumerate(samples, start=1):
            prompt += f"\n\n----------------\nEXAMPLE {i}:\n{sample}"

        return prompt
