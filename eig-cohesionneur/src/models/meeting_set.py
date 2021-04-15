from typing import List
from .meeting import Meeting


class MeetingSet:
    def __init__(self, meetings: List[Meeting] = None):
        if meetings:
            self.meetings = sorted(meetings, key=lambda m: str(m))
        else:
            self.meetings = set()

        self.meetings_hashes = set([m.get_hash() for m in self.meetings])

    def __contains__(self, meeting: Meeting) -> bool:
        return meeting.get_hash() in self.meetings_hashes

    def __iter__(self):
        return self.meetings.__iter__()