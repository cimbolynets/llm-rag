from typing import List
from langchain_core.callbacks import BaseCallbackHandler

class MyCustomHandler(BaseCallbackHandler):
    def on_llm_start(self,
        _,
        prompts: List[str], **kwargs) -> None:
        print("Prompt:")
        print(prompts)