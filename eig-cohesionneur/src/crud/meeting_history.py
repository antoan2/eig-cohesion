from typing import List
from datetime import datetime

from models import Promo, WeeklyMeetings, Meeting, MeetingSet
from redis import Redis


MEETINGS_HISTORY_KEY_PREFIX = "meeting_history"


def read_history(promo: Promo, redis_server: Redis) -> MeetingSet:
    meeting_hashes = redis_server.sinter("meeting_history")
    meetings = []
    for meeting_hash in meeting_hashes:
        meeting_hash = meeting_hash.decode()
        meetings.append(
            Meeting.get_from_hash(meeting_hash=meeting_hash, done=True, promo=promo)
        )
    return MeetingSet(meetings=meetings)
