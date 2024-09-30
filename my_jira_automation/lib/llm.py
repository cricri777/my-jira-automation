import logging
from http.client import responses

from lib.http import post_request_bearer


class ChatGPT:

    CHAT_URL = "https://api.openai.com/v1/chat/completions"

    def __init__(self, open_ai_token: str):
        self.token = open_ai_token

    def generate_prompt(self, prompt: str):
        # TODO complete this
        logging.debug(f"requesting chaGPT prompt")
        data = {

        }
        response = post_request_bearer(self.CHAT_URL, bearer_token=self.token, prompt=prompt, data=data)
