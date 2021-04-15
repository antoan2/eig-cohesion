import pytest

from models import Meeting, MeetingSet, Promo, Eig
from core.meetings_generation import generate_random_meetings


@pytest.fixture
def eigs():
    return [
        Eig(name="eig 1", project="projet 1"),
        Eig(name="eig 2", project="projet 1"),
        Eig(name="eig 3", project="projet 1"),
        Eig(name="eig 1", project="projet 2"),
        Eig(name="eig 2", project="projet 2"),
        Eig(name="eig 3", project="projet 2"),
        Eig(name="eig 1", project="projet 3"),
        Eig(name="eig 2", project="projet 3"),
        Eig(name="eig 3", project="projet 3"),
        Eig(name="eig 1", project="projet 4"),
        Eig(name="eig 2", project="projet 4"),
        Eig(name="eig 3", project="projet 4"),
    ]


@pytest.fixture
def promo(eigs):
    return Promo(promo_number=4, eigs=eigs)


@pytest.fixture
def meetings_history(eigs):
    meetings = [
        Meeting(eigs[0], eigs[3], done=False),
        Meeting(eigs[4], eigs[8], done=False),
        Meeting(eigs[6], eigs[10], done=False),
        Meeting(eigs[9], eigs[2], done=False),
    ]
    return MeetingSet(meetings=meetings)


@pytest.mark.repeat(10)
def test_meeting_generation_card(promo, meetings_history):
    generated_meetings = generate_random_meetings(
        promo=promo, meetings_history=meetings_history
    )
    # Computing expected number of pairs
    number_of_eigs = len(promo.eigs)
    assert len(generated_meetings) == number_of_eigs / 2


@pytest.mark.repeat(10)
def test_meeting_generation_avoid_meeting_history(promo, meetings_history):
    generated_meetings = generate_random_meetings(
        promo=promo, meetings_history=meetings_history
    )
    print(meetings_history.meetings)
    for meeting in generated_meetings:
        print(meeting)
        assert meeting not in meetings_history
        meeting.done = not meeting.done
        print(meeting)
        assert meeting not in meetings_history


@pytest.mark.repeat(10)
def test_meeting_generation_avoid_same_project(promo, meetings_history):
    generated_meetings = generate_random_meetings(
        promo=promo, meetings_history=meetings_history
    )
    for meeting in generated_meetings:
        assert meeting.eig_1.project != meeting.eig_2.project