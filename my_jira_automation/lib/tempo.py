from lib import log
from lib.http import post_request_bearer, get_request_bearer

logger = log.get_logger(__name__)

TEMPO_BASE_URL = "https://api.tempo.io/core/3/worklogs"
class Tempo:

    def __init__(self, tempo_api_key, project_account_id):
        self.tempo_api_key = tempo_api_key
        self.project_account_id = project_account_id

    def add_worklog_safely(self,
                           issue_key: str,
                           worklog_date: str,
                           time_spent_seconds: int = 27000,
                           description: str = "",
                           start_time: str = "09:00:00"):
        """if some worklog(s) already exists to the worklog_date we do nothing, else add_worklog
        :param issue_key:
        :param worklog_date:
        :param time_spent_seconds:
        :param description:
        :param start_time:
        :return:
        """
        request_worklog_params = {
            "authorAccountId": self.project_account_id,
            "from": worklog_date,
            "to": worklog_date
        }
        worklogs_to_validate = get_request_bearer(url=TEMPO_BASE_URL,
                                                  bearer_token=self.tempo_api_key,
                                                  params=request_worklog_params)
        logger.debug(f"check entried hours in {worklogs_to_validate['results']}")
        if len(worklogs_to_validate["results"]) > 0:
            logger.info(f"Found some worklog(s) in Tempo at the date={worklog_date} so we don't add anything")
            return None
        else:
            return self.add_worklog(issue_key=issue_key,
                                    worklog_date=worklog_date,
                                    time_spent_seconds=time_spent_seconds,
                                    description=description,
                                    start_time=start_time)


    def add_worklog(self,
                    issue_key: str,
                    worklog_date: str,
                    time_spent_seconds: int = 27000,
                    description: str = "",
                    start_time: str = "09:00:00"):
        """
        :param issue_key: Key of the Jira issue to which the worklog is to be added.
        :param worklog_date: Date for the worklog entry in YYYY-MM-DD format.
        :param time_spent_seconds: Amount of time spent on the issue in seconds. Default is 27000 (7.5 hours).
        :param description: Description or comment for the worklog. Default is an empty string.
        :param start_time: Start time of the worklog in HH:MM:SS format. Default is "09:00:00".
        :return: Response from the POST request to Tempo API with the provided worklog details.
        """
        payload = {
            "authorAccountId": self.project_account_id,
            "issueKey": issue_key,
            "timeSpentSeconds": time_spent_seconds,
            "startDate": worklog_date,
            "startTime": start_time,
            "description": description
        }
        logger.debug(f"add tempo workload with payload={payload}")
        return post_request_bearer(url=TEMPO_BASE_URL,bearer_token=self.tempo_api_key, data=payload)