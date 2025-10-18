from datetime import datetime

import pytest

from lib.date import quebec_working_day_of_current_week


@pytest.mark.parametrize(
    "day, list_work_day_expected",
    [
        (
            datetime(2020, 5, 16),
            ["2020-05-11", "2020-05-12", "2020-05-13", "2020-05-14", "2020-05-15"],
        ),
        # saint jean baptiste 24 juin 2026
        (datetime(2024, 6, 25), ["2024-06-25", "2024-06-26", "2024-06-27", "2024-06-28"]),
        # boxing day 26 december 2022
        (datetime(2022, 12, 26), ["2022-12-27", "2022-12-28", "2022-12-29", "2022-12-30"]),
        # vendredi saint vendredi 3 avril 2026
        (datetime(2025, 4, 15), ["2025-04-14", "2025-04-15", "2025-04-16", "2025-04-17"]),
    ],
)
def test_get_all_working_days_of_current_week(day, list_work_day_expected):
    list_working_day = quebec_working_day_of_current_week(day)
    assert list_working_day == list_work_day_expected
