import logging
import os

from lib.jira import Jira
from lib.openai import ChatGPT
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

    yaml_config = YamlConfig()
    configuration = yaml_config.get_config()

    dataeng_prompt = configuration["jira"]["prompt"][0]["dataEngineer"]
    chatGPT = ChatGPT(openai_api_key)

    jira_tickets_info = chatGPT.generate_prompt(dataeng_prompt)['choices'][0]['message']['content']

    # create ticket with jira
    for jira_ticket_info in jira_tickets_info:
        jira_response = jira_client.create_ticket(jira_ticket_info)
        logging.info(jira_response)



if __name__ == '__main__':
    run()