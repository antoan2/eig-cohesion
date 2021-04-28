from redis import Redis
from models import Meeting, Promo, WeeklyMeetings
import redis


def push_meeting_to_history(meeting: Meeting, promo: Promo, redis_server: Redis):
    redis_server.sadd(f"meeting_history:{promo.promo_number}", meeting.get_hash())


def create_on_weekly_meetings(
    meeting: Meeting, weekly_meetings_key: str, redis_server: Redis
) -> None:
    if meeting.done:
        done = "1"
    else:
        done = "0"
    redis_server.hset(weekly_meetings_key, meeting.get_hash(), done)
