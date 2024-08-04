from typing import List, Dict
from src.Vectordb import Vectordb
from transformers import pipeline

BASE_PROMPT = """You are responsible for answering questions about BLOOD DONATION. 
Please keep your answers concise and objective. Use the given examples to base your knowledge and formulate the final answer.
If you don't know the answer, DO NOT create one. Instead, suggest the user to look for the information in official websites."""


class Chat:
    def __init__(self) -> None:
        self.vectordb = Vectordb()
        self.pipe = pipeline(
            "text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0"
        )

    def ask(self, question: str) -> str:
        samples = self._get_related_samples(question)
        prompt = self._build_prompt(samples)
        result = self.pipe(
            [{"role": "system", "content": prompt}, {"role": "user", "content": question}]
        )
        answer = result[0]['generated_text'][-1]['content']
        return answer, samples

    def _get_related_samples(self, question: str) -> List[Dict]:
        return self.vectordb.retrieve(question)

    def _build_prompt(self, samples: List[str]) -> str:
        prompt = BASE_PROMPT

        for i, sample in enumerate(samples, start=1):
            prompt += f"\n\n----------------\nEXAMPLE {i}:\n{sample}"

        return prompt
