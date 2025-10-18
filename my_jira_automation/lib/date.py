from datetime import datetime, timedelta

import holidays

from lib import log

logger = log.get_logger(__name__)


def quebec_working_day_of_current_week(day: datetime = datetime.now()) -> list:
    """
    day: default is today, get all the working day of the week of this day
    :return: A list of strings representing the dates for the working days given a current day (Monday to Friday)
    format 'YYYY-MM-DD'

    Notes: We exclude Quebec holiday !
    """
    start_of_week = day - timedelta(days=day.weekday())
    logger.debug(f"start_of_week={start_of_week}")
    weekdays = [start_of_week + timedelta(days=i) for i in range(5)]

    weekday_without_holiday = []

    # exclude holidays
    for day in weekdays:
        quebec_holiday = holidays.country_holidays(country="CA", subdiv="QC", years=day.year)
        if day in quebec_holiday:
            logger.info(f"day {day} is a quebec holiday, skipping")
        else:
            weekday_without_holiday.append(day)

    return [day.strftime("%Y-%m-%d") for day in weekday_without_holiday]
