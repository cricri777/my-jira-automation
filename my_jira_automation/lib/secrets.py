import base64
import json
import logging
import os

import boto3
from mypy_boto3_secretsmanager.client import SecretsManagerClient

logger = logging.getLogger(__name__)

class Secrets:
    """get secrets for API jira, tempo, openai from secretmanager or default environment variable"""
    def __init__(self, is_secret_manager: bool):
        if is_secret_manager:
            logger.info("fetching configuration from awssecrets")
            session = boto3.session.Session()
            client: SecretsManagerClient = session.client(service_name="secretsmanager", region_name="ca-central-1")
            response = client.get_secret_value(SecretId="my-jira-automation")
            secret = json.loads(response["SecretString"])
            self._jira_api_token = base64.b64decode(secret.get("JIRA_API_TOKEN"))
            self._openai_api_key = base64.b64decode(secret.get("OPENAI_API_KEY"))
            self._tempo_api_key = base64.b64decode(secret.get("TEMPO_API_KEY"))
        else:
            logger.info("fetching configuration from env variables")
            self._jira_api_token = os.getenv("JIRA_API_TOKEN")
            self._openai_api_key = os.getenv("OPENAI_API_KEY")
            self._tempo_api_key = os.getenv("TEMPO_API_KEY")

    @property
    def jira_api_token(self):
        return self._jira_api_token

    @property
    def openai_api_key(self):
        return self._openai_api_key

    @property
    def tempo_api_key(self):
        return self._tempo_api_key
