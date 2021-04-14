from __future__ import annotations

from datetime import date
from redis import Redis
from typing import List
from core.eig import Eig

class Meeting:
    def __init__(self, eig_1: Eig, eig_2: Eig, done: bool=False):
        self.eig_1 = eig_1
        self.eig_2 = eig_2
        self.done = done
    
    def __repr__(self):
        print(sorted([repr(self.eig_1), repr(self.eig_2)]))
        return ' VS '.join(sorted([repr(self.eig_1), repr(self.eig_2)]))

    def set_done(self):
        self.done = True

    def set_not_done(self):
        self.done = False
    
    def eig_participate(self, eig: Eig) -> bool:
        return (eig.get_hash() == self.eig_1.get_hash()) or (eig.get_hash() == self.eig_2.get_hash())

    def overlap(self, meeting: Meeting) -> bool:
        return (self.eig_participate(meeting.eig_1) or self.eig_participate(meeting.eig_2))
    
    def get_hash(self):
        return '_'.join(sorted([self.eig_1.get_hash(), self.eig_2.get_hash()]))
    
    
class MeetingsList:
    def __init__(self, meetings: List[Meeting]=None):
        if meetings:
            self.meetings = sorted(meetings, key=lambda m: str(m))
        else:
            self.meetings = []

        self.meetings_hashes = [m.get_hash() for m in self.meetings]
    
    def __contains__(self, meeting: Meeting) -> bool:
        return meeting.get_hash() in self.meetings_hashes

    def __iter__(self):
        return self.meetings.__iter__()

class WeeklyMeetings(MeetingsList):
    def __init__(self, start_date: date, end_date: date, meetings: List[Meeting]=None):
        super().__init__(meetings=meetings)
        self.start_date = start_date
        self.end_date = end_date

    def get_dates_slug(self):
        date_format = '%Y-%m-%d'
        return '_'.join((self.start_date.strftime(date_format), self.end_date.strftime(date_format)))

    def get_progres(self):
        return 100 * (
            sum([meeting.done for meeting in self.meetings])
            / len(self.meetings)
        )