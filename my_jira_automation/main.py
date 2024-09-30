import logging
import os

from lib.jira import Jira
from lib.llm import ChatGPT
from lib.yaml import YamlConfig


def run():

    jira_base_url = os.getenv("JIRA_BASE_URL")
    jira_username = os.getenv("JIRA_USERNAME")
    jira_api_token = os.getenv("JIRA_API_TOKEN")
    jira_project_id = os.getenv("JIRA_PROJECT_ID")
    # aws_profile = os.getenv("AWS_PROFILE")
    # jira_account_id = os.getenv("JIRA_ACCOUNT_ID")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    # tempo_api_key = os.getenv("TEMPO_API_KEY")

    logging.info(f"jira ticket automation: jira_url={jira_base_url}, jira_user={jira_username}, jira_token=REDACTED")
    jira_client = Jira(jira_base_url=jira_base_url,
                       jira_username=jira_username,
                       jira_api_token=jira_api_token,
                       jira_project_id=jira_project_id)
    print(jira_client.get_ticket("BDEP-2"))

    # TODO link chatgpt
    # TODO read config file
    yaml_config = YamlConfig()
    configuration = yaml_config.get_config()
    print(yaml_config.get_config())
    # chat_gpt = ChatGPT(openai_api_key)
    # chat_gpt.generate_prompt()

if __name__ == '__main__':
    run()