from __future__ import annotations
from typing import List
from datetime import date

from .meeting_set import MeetingSet
from .meeting import Meeting


class WeeklyMeetings(MeetingSet):
    def __init__(
        self, start_date: date, end_date: date, meetings: List[Meeting] = None
    ):
        super().__init__(meetings=meetings)
        self.start_date = start_date
        self.end_date = end_date

    def __eq__(self, other: WeeklyMeetings):
        if isinstance(other, WeeklyMeetings):
            return (
                (self.start_date == other.start_date)
                and (self.end_date == other.end_date)
                and (self.meetings == other.meetings)
            )
        return False

    def get_dates_slug(self):
        date_format = "%Y-%m-%d"
        return "_".join(
            (self.start_date.strftime(date_format), self.end_date.strftime(date_format))
        )

    def get_progres(self):
        return 100 * (
            sum([meeting.done for meeting in self.meetings]) / len(self.meetings)
        )