from typing import List, Dict
from src.Vectordb import Vectordb
from transformers import pipeline

BASE_PROMPT = {
    "redcross": """You are responsible for answering questions about BLOOD DONATION. 
The following examples must be aligned to your answer. Use them to base your knowledge and formulate the final answer.
If you don't know the answer, DO NOT create one, just say you don't know.""",
    "hemocentro": """Você é responsável por responder perguntas sobre DOAÇÃO DE SANGUE.
O exemplos fornecidos a seguir devem estar alinhados com a sua resposta. Use-os para basear o seu conhecimento e formular sua resposta final.
Se você não souber a resposta, NÃO invente, apenas diga que não sabe.""",
}


class Chat:
    def __init__(self, source: str) -> None:
        self.source = source
        self.vectordb = Vectordb(name=source)
        self.pipe = pipeline(
            "text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0"
        )

    def ask(self, question: str) -> str:
        samples = self._get_related_samples(question)
        prompt = self._build_prompt(samples)
        result = self.pipe(
            [
                {"role": "system", "content": prompt},
                {"role": "user", "content": question},
            ],
            max_new_tokens=1024,
        )

        answer = result[0]["generated_text"][-1]["content"]
        return answer, samples

    def _get_related_samples(self, question: str) -> List[Dict]:
        return self.vectordb.retrieve(question)

    def _build_prompt(self, samples: List[str]) -> str:
        prompt = BASE_PROMPT[self.source]

        for i, sample in enumerate(samples, start=1):
            prompt += f"\n\n----------------\nEXAMPLE {i}:\n{sample}"

        return prompt
