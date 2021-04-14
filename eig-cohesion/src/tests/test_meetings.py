from datetime import date
import pytest
from core.meetings import MeetingsList, Meeting, WeeklyMeetings
from core.eig import Eig

def test_meeting_participate():
    eig_1 = Eig(name='eig 1', project='project 1')
    eig_2 = Eig(name='eig 2', project='project 2')
    eig_3 = Eig(name='eig 3', project='project 3')
    
    meeting = Meeting(eig_1=eig_1, eig_2=eig_2)
    assert meeting.eig_participate(eig_1)
    assert meeting.eig_participate(eig_2)
    assert not meeting.eig_participate(eig_3)

def test_meeting_overlap():
    eig_1 = Eig(name='eig 1', project='project 1')
    eig_2 = Eig(name='eig 2', project='project 2')
    eig_3 = Eig(name='eig 3', project='project 3')
    eig_4 = Eig(name='eig 4', project='project 3')
    
    meeting_1 = Meeting(eig_1=eig_1, eig_2=eig_2)
    meeting_2 = Meeting(eig_1=eig_1, eig_2=eig_3)
    meeting_3 = Meeting(eig_1=eig_3, eig_2=eig_4)
    assert meeting_1.overlap(meeting_2)
    assert not meeting_1.overlap(meeting_3)

def test_meeting_history_contains():
    eig_1 = Eig(name='eig 1', project='project 1')
    eig_2 = Eig(name='eig 2', project='project 2')
    eig_3 = Eig(name='eig 3', project='project 3')

    meetings_history = MeetingsList(meetings=[Meeting(eig_1=eig_1, eig_2=eig_2)])
    assert Meeting(eig_1=eig_1, eig_2=eig_2) in meetings_history
    # Reversed meeting
    assert Meeting(eig_1=eig_2, eig_2=eig_1) in meetings_history
    assert Meeting(eig_1=eig_2, eig_2=eig_3) not in meetings_history

def test_weekly_meetings_date_slug():
    weekly_meetings = WeeklyMeetings(start_date=date(year=2021, month=1, day=12),end_date=date(year=2021, month=1, day=23))
    assert weekly_meetings.get_dates_slug() == '2021-01-12_2021-01-23'


