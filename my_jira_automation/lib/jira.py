import logging

from lib.http import get_request, post_request


class Jira:
# TODO create ticket
# TODO get ticket

    def __init__(self, jira_base_url: str,
                 jira_username: str,
                 jira_api_token: str,
                 jira_project_id: str):
        logging.debug(f"Create jira object with jira_user={jira_username}"
                      f", jira_toker=REDACTED,"
                      f" jira_project_id={jira_project_id}")
        self.jira_base_url = jira_base_url
        self.jira_api_token = jira_api_token
        self.jira_user_name = jira_username
        self.jira_project_id = jira_project_id

    def get_ticket(self, ticket_id: str):
        jira_url = f"{self.jira_base_url}/rest/api/2/issue/{ticket_id}"
        jira_json_response = get_request(jira_url, self.jira_user_name, self.jira_api_token)
        logging.info(f"received jira response {jira_json_response}")
        return jira_json_response


    def create_ticket(self, summary: str, description: str):
        logging.debug(f"creating ticket with summary {summary}, description {description}")
        jira_url = f"{self.jira_base_url}/rest/api/2/issue"
        body = f"""
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
                "summary": "{summary}",
                "description": "{description}"
            }
        """

        jira_json_response = post_request(jira_url, self.jira_user_name, self.jira_api_token, body)
        logging.info(f"created ticket response={jira_json_response}")
