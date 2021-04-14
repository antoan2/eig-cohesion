from datetime import date
from core.data_loading import load_promo
from core.redis_utils import redis_server, load_history
import core.redis_utils as ru
from core.meetings_generation import generate_random_meetings
from core.meetings import Meeting, MeetingsList, WeeklyMeetings
from core.redis_utils import add_weekly_meetings, load_weekly_meetings

promo = load_promo(4)
meetings_history = load_history(promo, redis_server)
meetings = generate_random_meetings(promo=promo, meetings_history=meetings_history)
meetings_history = MeetingsList(meetings=meetings_history.meetings + meetings)
print(meetings)
meetings = generate_random_meetings(promo=promo, meetings_history=meetings_history)
meetings_history = MeetingsList(meetings=meetings_history.meetings + meetings)
print(meetings)
meetings = generate_random_meetings(promo=promo, meetings_history=meetings_history)
meetings_history = MeetingsList(meetings=meetings_history.meetings + meetings)
print(meetings)

w_1 = WeeklyMeetings(start_date=date(2021, 12, 9), end_date=date(2021, 12, 15), meetings=meetings)
add_weekly_meetings(promo=promo, weekly_meetings=w_1, redis_server=redis_server)
print(list(ru.get_all_weekly_meetings(promo, redis_server)))
key = list(ru.get_all_weekly_meetings(promo, redis_server))[0]
print(key)
w_2 = load_weekly_meetings(weekly_meetings_key=key, promo=promo, redis_server=redis_server)
print(ru.get_all_weekly_meetings(promo, redis_server))