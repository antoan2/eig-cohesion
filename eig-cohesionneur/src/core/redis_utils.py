from redis import Redis
from models import Meeting


def push_meeting_to_history(meeting: Meeting, redis_server: Redis):
    redis_server.sadd("meeting_history", meeting.get_hash())
