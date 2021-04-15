from redis import Redis
from models import Meeting, Promo


def push_meeting_to_history(meeting: Meeting, promo: Promo, redis_server: Redis):
    redis_server.sadd(f"meeting_history:{promo.promo_number}", meeting.get_hash())