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
                           description: str = ""):
        """if some worklog(s) already exists to the worklog_date we do nothing,
        else add_worklog
        :param issue_key:
        :param worklog_date:
        :param time_spent_seconds:
        :param description:
        :return:
        """
        request_worklog_params = {
            "authorAccountId": self.project_account_id,
            "from": worklog_date,
            "to": worklog_date
        }
        worklogs_to_validate = get_request_bearer(url=TEMPO_BASE_URL, bearer_token=self.tempo_api_key, params=request_worklog_params)
        logger.debug(f"check entried hours in {worklogs_to_validate}")
        if len(worklogs_to_validate) > 0:
            logger.info(f"Found some worklog(s) in Tempo at the date={worklog_date} so we don't add anything")
            return None
        else:
            return self.add_worklog(issue_key=issue_key, worklog_date=worklog_date)


    def add_worklog(self,
                    issue_key: str,
                    worklog_date: str,
                    time_spent_seconds: int = 27000,
                    description: str = ""):
        payload = {
            "authorAccountId": self.project_account_id,
            "issueKey": issue_key,
            "timeSpentSeconds": time_spent_seconds,
            "startDate": worklog_date,
            "startTime": "09:00:00",
            "description": description
        }
        logger.debug(f"add tempo workload with payload={payload}")
        return post_request_bearer(url=TEMPO_BASE_URL,bearer_token=self.tempo_api_key, data=payload)