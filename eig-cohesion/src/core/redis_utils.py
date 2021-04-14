from datetime import datetime
from typing import List
import redis
from redis import Redis
from core.promo import Promo
from core.meetings import Meeting, WeeklyMeetings, MeetingsList

DATE_FORMAT = "%Y-%m-%d"


def get_redis_server() -> Redis:
    return Redis(host="redis")


redis_server = get_redis_server()


def push_meeting_to_history(meeting: Meeting, redis_server: Redis):
    redis_server.sadd("meeting_history", meeting.get_hash())


def get_all_weekly_meetings(promo: Promo, redis_server: Redis) -> List[str]:
    return [
        key.decode()
        for key in redis_server.scan_iter(f"weekly_meetings_{promo.promo_number}:*")
    ]


def get_weekly_meetings_key(promo: Promo, weekly_meetings: WeeklyMeetings) -> str:
    return f"weekly_meetings_{promo.promo_number}:{weekly_meetings.get_dates_slug()}"


def get_start_date_from_weekly_meetings_key(weekly_meetings_key: str) -> str:
    dates_str = weekly_meetings_key.split(":")[1]
    start_date_str = dates_str.split("_")[0]
    return datetime.strptime(start_date_str, DATE_FORMAT).date()


def get_end_date_from_weekly_meetings_key(weekly_meetings_key: str) -> str:
    dates_str = weekly_meetings_key.split(":")[1]
    end_date_str = dates_str.split("_")[1]
    return datetime.strptime(end_date_str, DATE_FORMAT).date()


def add_weekly_meetings(
    weekly_meetings: WeeklyMeetings, promo: Promo, redis_server: Redis
):
    weekly_meetings_key = get_weekly_meetings_key(
        weekly_meetings=weekly_meetings, promo=promo
    )
    redis_server.delete(weekly_meetings_key)
    for meeting in weekly_meetings.meetings:
        redis_server.hset(weekly_meetings_key, meeting.get_hash(), 0)


def set_meeting_done(
    meeting_hash: str, weekly_meetings_key: str, redis_server: redis_server
):
    redis_server.hset(weekly_meetings_key, meeting_hash, '1')


def set_meeting_not_done(
    meeting_hash: str, weekly_meetings_key: str, redis_server: redis_server
):
    redis_server.hset(weekly_meetings_key, meeting_hash, '0')


def get_meeting_from_hash(meeting_hash: str, done: str, promo: Promo) -> Meeting:
    eig_1_hash, eig_2_hash = meeting_hash.split("_")
    if done == "0":
        done = False
    else:
        done = True
    return Meeting(promo.get_eig(eig_1_hash), promo.get_eig(eig_2_hash), done)


def load_weekly_meetings(weekly_meetings_key: str, promo: Promo, redis_server: Redis):
    meeting_hashes = redis_server.hscan_iter(weekly_meetings_key)
    meetings = []
    for meeting_hash, done in meeting_hashes:
        meeting_hash = meeting_hash.decode()
        done = done.decode()
        meetings.append(
            get_meeting_from_hash(meeting_hash=meeting_hash, done=done, promo=promo)
        )
    return WeeklyMeetings(
        start_date=get_start_date_from_weekly_meetings_key(weekly_meetings_key),
        end_date=get_end_date_from_weekly_meetings_key(weekly_meetings_key),
        meetings=meetings,
    )


def load_history(promo: Promo, redis_server: Redis) -> MeetingsList:
    meeting_hashes = redis_server.sinter("meeting_history")
    meetings = []
    for meeting_hash in meeting_hashes:
        meeting_hash = meeting_hash.decode()
        meetings.append(
            get_meeting_from_hash(meeting_hash=meeting_hash, done="1", promo=promo)
        )
    return MeetingsList(meetings=meetings)
