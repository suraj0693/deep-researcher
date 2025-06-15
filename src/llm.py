# A litellm based llm wrapper

from litellm import completion


class LLM:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def run(self, prompt: str):
        self.kwargs.update(messages=[{"role": "user", "content": prompt}])
        return completion(
            self.kwargs
        )
