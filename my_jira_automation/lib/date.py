from datetime import datetime, timedelta

from lib import log

logger = log.get_logger(__name__)

def get_weekdays() -> list:
    """
    :return: A list of strings representing the dates for the weekdays (Monday to Friday)
    of the current week in 'YYYY-MM-DD' format.
    """
    logger.debug("getting weekday")
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday())
    logger.debug(f"start_of_week={start_of_week}")
    weekdays = [start_of_week + timedelta(days=i) for i in range(5)]
    logger.debug(f"weekdays={weekdays}")
    return [day.strftime('%Y-%m-%d') for day in weekdays]
