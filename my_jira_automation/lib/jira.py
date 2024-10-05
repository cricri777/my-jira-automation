import json

from lib import log
from lib.http import get_request, post_request

logger = log.get_logger(__name__)

class Jira:
    """
    Jira is a class to interact with the JIRA REST API.

    :param jira_base_url: The base URL for the JIRA instance.
    :type jira_base_url: str
    :param jira_username: The username for JIRA authentication.
    :type jira_username: str
    :param jira_api_token: The API token for JIRA authentication.
    :type jira_api_token: str
    :param jira_project_id: The project ID in JIRA where operations will be performed.
    :type jira_project_id: str
    """

    def __init__(self, jira_base_url: str,
                 jira_username: str,
                 jira_api_token: str,
                 jira_project_id: str):
        logger.debug(f"Create jira object with jira_user={jira_username}"
                      f", jira_toker=REDACTED,"
                      f" jira_project_id={jira_project_id}")
        self._jira_base_url = jira_base_url
        self._jira_api_token = jira_api_token
        self._jira_user_name = jira_username
        self._jira_project_id = jira_project_id

    def get_ticket(self, ticket_id: str):
        """
        :param ticket_id: The unique identifier of the JIRA ticket.
        :return: A JSON response containing the details of the specified JIRA ticket.
        """
        jira_url = f"{self._jira_base_url}/rest/api/2/issue/{ticket_id}"
        jira_json_response = get_request(jira_url, self._jira_user_name, self._jira_api_token)
        logger.info(f"received jira response {jira_json_response}")
        return jira_json_response


    def create_ticket(self, summary: str, description: str):
        """
        :param summary: The summary or title of the ticket to be created.
        :param description: A detailed description of the ticket.
        :return: The JSON response received from the JIRA API after creating the ticket.
        """
        logger.debug(f"creating ticket with summary={summary}, description={description}")
        jira_url = f"{self._jira_base_url}/rest/api/2/issue"
        body = {
            "fields": {
                "issuetype": {
                    "name": "Story"
                },
                "parent": {
                    "key": "BDEP-2"
                },
                "project": {
                    "key": "BDEP"
                },
                "summary": f"{summary}",
                "description": f"{description}"
            }
        }


        jira_json_response = post_request(jira_url, self._jira_user_name, self._jira_api_token, body)
        logger.info(f"created ticket response={jira_json_response}")
        return jira_json_response
