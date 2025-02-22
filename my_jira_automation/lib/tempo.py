from lib import log
from lib.http import post_request_bearer, get_request_bearer

logger = log.get_logger(__name__)

class Tempo:

    def __init__(self,
                 tempo_api_key,
                 project_account_id,
                 tempo_base_url="https://api.tempo.io/4/worklogs"
                 ):
        self.tempo_api_key = tempo_api_key
        self.project_account_id = project_account_id
        self.tempo_base_url = tempo_base_url

    def is_week_almost_full(self, weekdays: list):
        """if current week in tempo is have more than 30 hours logged in, then we return False
        else True

        :param weekdays:
        :return:
        """
        assert len(weekdays) == 5, "weekdays should be 5"
        request_worklog_params = {
            "authorAccountId": self.project_account_id,
            "from": weekdays[0],
            "to": weekdays[-1]
        }
        worklogs_to_validate = get_request_bearer(url=self.tempo_base_url,
                                                  bearer_token=self.tempo_api_key,
                                                  params=request_worklog_params)
        total_work_time_of_current_week = 0
        for worklog in worklogs_to_validate["results"]:
            total_work_time_of_current_week += worklog.get("timeSpentSeconds", 0)

        if total_work_time_of_current_week > 108000:
            logger.info(f"more than 30 hours logged this week, ({total_work_time_of_current_week} seconds)")
            return True
        else:
            logger.info(f"less than 30 hours logged this week, ({total_work_time_of_current_week} seconds)")
            return False

    def add_worklog_safely(self,
                           issue_id: str,
                           worklog_date: str,
                           time_spent_seconds: int = 27000,
                           description: str = "",
                           start_time: str = "09:00:00"):
        """if some worklog(s) already exists to the worklog_date we do nothing, else add_worklog
        :param issue_id:
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
        worklogs_to_validate = get_request_bearer(url=self.tempo_base_url,
                                                  bearer_token=self.tempo_api_key,
                                                  params=request_worklog_params)
        logger.debug(f"check entried hours in {worklogs_to_validate['results']}")
        if len(worklogs_to_validate["results"]) > 0:
            logger.info(f"Found some worklog(s) in Tempo at the date={worklog_date} so we don't add anything")
            return None
        else:
            return self.add_worklog(issue_id=issue_id,
                                    worklog_date=worklog_date,
                                    time_spent_seconds=time_spent_seconds,
                                    description=description,
                                    start_time=start_time)


    def add_worklog(self,
                    issue_id: str,
                    worklog_date: str,
                    time_spent_seconds: int = 27000,
                    description: str = "",
                    start_time: str = "09:00:00"):
        """
        :param issue_id: Key of the Jira issue to which the worklog is to be added.
        :param worklog_date: Date for the worklog entry in YYYY-MM-DD format.
        :param time_spent_seconds: Amount of time spent on the issue in seconds. Default is 27000 (7.5 hours).
        :param description: Description or comment for the worklog. Default is an empty string.
        :param start_time: Start time of the worklog in HH:MM:SS format. Default is "09:00:00".
        :return: Response from the POST request to Tempo API with the provided worklog details.
        """
        payload = {
            "authorAccountId": self.project_account_id,
            "issueId": issue_id,
            "timeSpentSeconds": time_spent_seconds,
            "startDate": worklog_date,
            "startTime": start_time,
            "description": description
        }
        logger.debug(f"add tempo workload with payload={payload}")
        return post_request_bearer(url=self.tempo_base_url,bearer_token=self.tempo_api_key, data=payload)