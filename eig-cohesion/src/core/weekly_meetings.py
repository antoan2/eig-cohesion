from typing import List
from datetime import date

class WeeklyMeetings:
    def __init__(self, start_date: date, end_date: date, meetings: List = None):
        start_date = date
        end_date = date
        if meetings:
            self.meetings = meetings
        else:
            self.meetings = []
