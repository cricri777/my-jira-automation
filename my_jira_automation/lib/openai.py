
from lib import log
from lib.http import post_request_bearer
logger = log.get_logger(__name__)

class ChatGPT:

    CHAT_URL = "https://api.openai.com/v1/chat/completions"

    def __init__(self, open_ai_token: str):
        self._token = open_ai_token

    def generate_prompt(self, prompt: str):
        logger.debug(f"requesting chaGPT prompt")
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
