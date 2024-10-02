import json

from lib import log

import os

from lib.date import get_weekdays
from lib.jira import Jira
from lib.openai import ChatGPT
from lib.tempo import Tempo
from lib.yaml import YamlConfig


logger = log.get_logger(__name__)

def run():

    jira_base_url = os.getenv("JIRA_BASE_URL")
    jira_username = os.getenv("JIRA_USERNAME")
    jira_api_token = os.getenv("JIRA_API_TOKEN")
    jira_project_id = os.getenv("JIRA_PROJECT_ID")
    # aws_profile = os.getenv("AWS_PROFILE")
    jira_account_id = os.getenv("JIRA_ACCOUNT_ID")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    tempo_api_key = os.getenv("TEMPO_API_KEY")

    logger.info(f"jira ticket automation: jira_url={jira_base_url}, jira_user={jira_username}, jira_token=REDACTED")
    jira_client = Jira(jira_base_url=jira_base_url,
                       jira_username=jira_username,
                       jira_api_token=jira_api_token,
                       jira_project_id=jira_project_id)

    yaml_config = YamlConfig()
    configuration = yaml_config.get_config()

    dataeng_prompt = configuration["jira"]["prompt"][0]["dataEngineer"]
    chat_gpt = ChatGPT(openai_api_key)

    jira_tickets_info = json.loads(chat_gpt.generate_prompt(dataeng_prompt)["choices"][0]["message"]["content"])
    weekdays = get_weekdays()
    logger.debug(f"weekdays={weekdays}")
    tempo = Tempo(tempo_api_key=tempo_api_key, project_account_id=jira_account_id)
    for jira_ticket_info in jira_tickets_info["jira_tickets_info"]:
        logger.debug(jira_ticket_info)
        jira_response = jira_client.create_ticket(summary=jira_ticket_info["title"],
                                                  description=jira_ticket_info["description"])
        logger.info(f"{len(jira_response)} jira info response generated")
        # tempo_response = tempo.add_worklog_safely(issue_key=jira_ticket, worklog_date=weekdays[4])

if __name__ == "__main__":
    run()