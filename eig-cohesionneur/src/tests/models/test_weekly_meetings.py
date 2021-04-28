from datetime import date
from models import WeeklyMeetings


def test_weekly_meetings_date_slug():
    weekly_meetings = WeeklyMeetings(
        start_date=date(year=2021, month=1, day=12),
        end_date=date(year=2021, month=1, day=23),
    )
    assert weekly_meetings.get_dates_slug() == "2021-01-12_2021-01-23"
