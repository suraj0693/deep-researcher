## a litellm based llm wrapper

from litellm import completion

class LLM:
    def __init__(self, model: str):
        self.model = model

    def run(self, prompt: str):
        return completion(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
        )