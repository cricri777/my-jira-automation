import json
import os
import random

from lib import log
from lib.date import quebec_working_day_of_current_week
from lib.jira import Jira
from lib.openai import ChatGPT
from lib.secrets import Secrets
from lib.tempo import Tempo
from lib.yaml import YamlConfig

logger = log.get_logger(__name__)


def run(is_secret_manager=False):
    """Executes the main workflow for Jira ticket automation, which involves the following steps:
    1. Fetches environment variables required for Jira and OpenAI API authentication.
    2. Logs the initial configuration and credentials.
    3. Creates a Jira client instance using the provided credentials.
    4. Loads configuration from a YAML file.
    5. Generates a prompt for the data engineer role using OpenAI's ChatGPT.
    6. Parses the generated prompt to extract Jira ticket information.
    7. Iterates over the extracted ticket information to create Jira tickets using the Jira client.
    8. If the number of working_days is equal to 5, adds worklogs to Tempo for the created Jira tickets.

    :param is_secret_manager:
    :return: None
    """

    jira_base_url = os.getenv("JIRA_BASE_URL")
    jira_username = os.getenv("JIRA_USERNAME")
    jira_project_id = os.getenv("JIRA_PROJECT_ID")
    jira_account_id = os.getenv("JIRA_ACCOUNT_ID")
    tempo_base_url = os.getenv("TEMPO_BASE_URL")

    secrets = Secrets(is_secret_manager)
    jira_api_token, openai_api_key, tempo_api_key = (
        secrets.jira_api_token,
        secrets.openai_api_key,
        secrets.tempo_api_key,
    )

    working_days = quebec_working_day_of_current_week()
    logger.debug(f"working_days={working_days}")

    logger.info("validate if we need tempo is already filled")
    tempo = Tempo(
        tempo_api_key=tempo_api_key,
        project_account_id=jira_account_id,
        tempo_base_url=tempo_base_url,
    )
    if tempo.is_week_almost_full(working_days):
        logger.info("tempo is already filled for the week, closing now")
        return

    logger.info(
        f"jira ticket automation: jira_url={jira_base_url}, jira_user={jira_username}, jira_token=REDACTED"
    )
    jira_client = Jira(
        jira_base_url=jira_base_url,
        jira_username=jira_username,
        jira_api_token=jira_api_token,
        jira_project_id=jira_project_id,
    )

    yaml_config = YamlConfig()
    configuration = yaml_config.get_config()

    dataeng_prompt = configuration["jira"]["prompt"][0]["dataEngineer"]
    chat_gpt = ChatGPT(openai_api_key)
    chat_gpt_output = chat_gpt.generate_prompt(dataeng_prompt)

    logger.info(f"chat_gpt_output={chat_gpt_output['choices']}")
    jira_tickets_info = json.loads(chat_gpt_output["choices"][0]["message"]["content"])

    jira_tickets = list()
    for jira_ticket_info in jira_tickets_info["jira_tickets_info"]:
        logger.debug(jira_ticket_info)
        jira_response = jira_client.create_ticket(
            summary=jira_ticket_info["title"], description=jira_ticket_info["description"]
        )
        jira_tickets.append(jira_response["id"])

    # adding worklog to tempo to the jira tickets created above
    for working_day in working_days:
        logger.info(
            f"add tempo worklog: {tempo.add_worklog_safely(issue_id=random.choice(jira_tickets), worklog_date=working_day)}"
        )


if __name__ == "__main__":
    run()
