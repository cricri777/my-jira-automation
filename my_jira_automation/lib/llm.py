import logging

from lib.http import post_request_bearer


class ChatGPT:

    CHAT_URL = "https://api.openai.com/v1/chat/completions"

    def __init__(self, open_ai_token: str):
        self._token = open_ai_token

    def generate_prompt(self, prompt: str):
        logging.debug(f"requesting chaGPT prompt")
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful assistant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        return post_request_bearer(self.CHAT_URL, bearer_token=self._token, data=data)
