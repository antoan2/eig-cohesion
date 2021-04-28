from typing import List
from datetime import datetime

from models import Promo, WeeklyMeetings, Meeting
from redis import Redis
from crud.meeting import create_on_weekly_meetings
import redis


DATE_FORMAT = "%Y-%m-%d"
WEEKLY_MEETINGS_KEY_PREFIX = "weekly_meetings"


def get_key(
    weekly_meetings: WeeklyMeetings,
    promo: Promo,
    key_prefix: str = WEEKLY_MEETINGS_KEY_PREFIX,
) -> str:
    return f"{key_prefix}:{promo.promo_number}:{weekly_meetings.get_dates_slug()}"


def get_start_date_from_key(weekly_meetings_key: str) -> str:
    dates_str = weekly_meetings_key.split(":")[-1]
    start_date_str = dates_str.split("_")[0]
    return datetime.strptime(start_date_str, DATE_FORMAT).date()


def get_end_date_from_key(weekly_meetings_key: str) -> str:
    dates_str = weekly_meetings_key.split(":")[-1]
    end_date_str = dates_str.split("_")[1]
    return datetime.strptime(end_date_str, DATE_FORMAT).date()


def create(weekly_meetings: WeeklyMeetings, promo: Promo, redis_server: Redis) -> None:
    weekly_meetings_key = get_key(weekly_meetings=weekly_meetings, promo=promo)
    redis_server.delete(weekly_meetings_key)
    for meeting in weekly_meetings.meetings:
        create_on_weekly_meetings(
            meeting=meeting,
            weekly_meetings_key=weekly_meetings_key,
            redis_server=redis_server,
        )


def read(weekly_meetings_key: str, promo: Promo, redis_server: Redis):
    meeting_hashes = redis_server.hscan_iter(weekly_meetings_key)
    meetings = []
    for meeting_hash, done in meeting_hashes:
        meetings.append(
            get_meeting_from_redis(meeting_hash=meeting_hash, done=done, promo=promo)
        )
    return WeeklyMeetings(
        start_date=get_start_date_from_key(weekly_meetings_key),
        end_date=get_end_date_from_key(weekly_meetings_key),
        meetings=meetings,
    )


def read_all_keys(promo: Promo, redis_server: Redis) -> List[str]:
    return [
        key.decode()
        for key in redis_server.scan_iter(
            f"{WEEKLY_MEETINGS_KEY_PREFIX}:{promo.promo_number}:*"
        )
    ]


def read_all(promo: Promo, redis_server: Redis) -> List[WeeklyMeetings]:
    all_weekly_meetings = []
    for key in read_all_keys(promo=promo, redis_server=redis_server):
        all_weekly_meetings.append(
            read(weekly_meetings_key=key, promo=promo, redis_server=redis_server)
        )
    return all_weekly_meetings


def get_meeting_from_redis(meeting_hash: str, done: str, promo: Promo) -> Meeting:
    meeting_hash = meeting_hash.decode()
    done = done.decode()
    if done == "0":
        done = False
    else:
        done = True
    return Meeting.get_from_hash(meeting_hash=meeting_hash, done=done, promo=promo)


def set_meeting_done(
    meeting_hash: str, weekly_meetings_key: str, redis_server: Redis
) -> None:
    redis_server.hset(weekly_meetings_key, meeting_hash, "1")


def set_meeting_not_done(
    meeting_hash: str, weekly_meetings_key: str, redis_server: Redis
) -> None:
    redis_server.hset(weekly_meetings_key, meeting_hash, "0")


def set_current(
    weekly_meetings: WeeklyMeetings, promo: Promo, redis_server: Redis
) -> None:
    key = get_key(weekly_meetings=weekly_meetings, promo=promo)
    redis_server.set(f"current:{promo.promo_number}", key)


def read_current_key(promo: Promo, redis_server: Redis) -> WeeklyMeetings:
    key = redis_server.get(f"current:{promo.promo_number}")
    return key.decode()


def read_current(promo: Promo, redis_server: Redis) -> WeeklyMeetings:
    key = read_current_key(promo=promo, redis_server=redis_server)
    return read(weekly_meetings_key=key, promo=promo, redis_server=redis_server)


def read_all_except_current(promo: Promo, redis_server: Redis) -> List[WeeklyMeetings]:
    key = read_current_key(promo=promo, redis_server=redis_server)
    all_keys = read_all_keys(promo=promo, redis_server=redis_server)
    all_keys.remove(key)
    all_keys = sorted(
        all_keys, key=lambda key: get_start_date_from_key(key), reverse=True
    )
    return [read(c_key, promo=promo, redis_server=redis_server) for c_key in all_keys]
