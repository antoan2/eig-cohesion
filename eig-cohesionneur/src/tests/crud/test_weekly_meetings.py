from typing import List
from datetime import date
import pytest

import fakeredis
from models import Promo, WeeklyMeetings, Meeting, Eig
from crud.weekly_meetings import (
    get_key,
    get_start_date_from_key,
    get_end_date_from_key,
    create,
    read,
    read_all_keys,
    read_all,
    set_meeting_done,
    set_meeting_not_done,
    set_current,
    read_current,
)


@pytest.fixture
def redis_server() -> fakeredis.FakeStrictRedis:
    return fakeredis.FakeStrictRedis()


@pytest.fixture
def eigs() -> List[Eig]:
    eig_1 = Eig(name="n_1", project="p_1")
    eig_2 = Eig(name="n_2", project="p_2")
    eig_3 = Eig(name="n_3", project="p_2")
    return [eig_1, eig_2, eig_3]


@pytest.fixture
def weekly_meetings(eigs) -> WeeklyMeetings:
    start_date = date(year=2012, month=1, day=2)
    end_date = date(year=2013, month=2, day=3)
    meetings = [
        Meeting(eig_1=eigs[0], eig_2=eigs[1], done=False),
        Meeting(eig_1=eigs[0], eig_2=eigs[2], done=True),
    ]

    weekly_meetings = WeeklyMeetings(
        start_date=start_date, end_date=end_date, meetings=meetings
    )
    return weekly_meetings


@pytest.fixture
def promo(eigs) -> Promo:
    return Promo(promo_number=10, eigs=eigs)


def test_get_key():
    promo = Promo(promo_number=10)
    weekly_meetings = WeeklyMeetings(
        start_date=date(year=2012, month=1, day=2),
        end_date=date(year=2013, month=2, day=3),
    )
    key = get_key(
        weekly_meetings=weekly_meetings, promo=promo, key_prefix="defined_prefix"
    )

    expected_key = "defined_prefix:10:2012-01-02_2013-02-03"
    assert key == expected_key


def test_get_start_end_date_from_key():
    key = "prefix:promo:2012-01-03_2013-02-04"
    start_date = get_start_date_from_key(key)
    end_date = get_end_date_from_key(key)
    assert start_date == date(year=2012, month=1, day=3)
    assert end_date == date(year=2013, month=2, day=4)


def test_create_read(weekly_meetings, promo, redis_server):
    create(weekly_meetings=weekly_meetings, promo=promo, redis_server=redis_server)
    key = get_key(weekly_meetings, promo=promo)
    weekly_meetings_read = read(
        weekly_meetings_key=key, promo=promo, redis_server=redis_server
    )
    assert weekly_meetings == weekly_meetings_read


def test_set_meeting_done(weekly_meetings, promo, redis_server):
    create(weekly_meetings=weekly_meetings, promo=promo, redis_server=redis_server)
    key = get_key(weekly_meetings, promo=promo)

    set_meeting_done(weekly_meetings.meetings[0].get_hash(), key, redis_server)
    set_meeting_done(weekly_meetings.meetings[1].get_hash(), key, redis_server)

    weekly_meetings_read = read(
        weekly_meetings_key=key, promo=promo, redis_server=redis_server
    )
    assert weekly_meetings_read.meetings[0].done
    assert weekly_meetings_read.meetings[1].done


def test_set_meeting_not_done(weekly_meetings, promo, redis_server):
    create(weekly_meetings=weekly_meetings, promo=promo, redis_server=redis_server)
    key = get_key(weekly_meetings, promo=promo)

    set_meeting_not_done(weekly_meetings.meetings[0].get_hash(), key, redis_server)
    set_meeting_not_done(weekly_meetings.meetings[1].get_hash(), key, redis_server)

    weekly_meetings_read = read(
        weekly_meetings_key=key, promo=promo, redis_server=redis_server
    )
    assert not weekly_meetings_read.meetings[0].done
    assert not weekly_meetings_read.meetings[1].done


def test_read_all_keys(weekly_meetings, promo, redis_server):
    w_1 = WeeklyMeetings(
        start_date=date(year=2020, month=1, day=1),
        end_date=date(year=2020, month=2, day=1),
        meetings=[Meeting(eig_1=promo.eigs[0], eig_2=promo.eigs[1])],
    )
    w_2 = WeeklyMeetings(
        start_date=date(year=2020, month=2, day=1),
        end_date=date(year=2020, month=3, day=1),
        meetings=[Meeting(eig_1=promo.eigs[0], eig_2=promo.eigs[2])],
    )
    create(weekly_meetings=w_1, promo=promo, redis_server=redis_server)
    create(weekly_meetings=w_2, promo=promo, redis_server=redis_server)

    all_keys = read_all_keys(promo=promo, redis_server=redis_server)
    assert all_keys == [
        get_key(w_1, promo=promo),
        get_key(w_2, promo=promo),
    ]


def test_read_all(promo, redis_server):
    w_1 = WeeklyMeetings(
        start_date=date(year=2020, month=1, day=1),
        end_date=date(year=2020, month=2, day=1),
        meetings=[Meeting(eig_1=promo.eigs[0], eig_2=promo.eigs[1])],
    )
    w_2 = WeeklyMeetings(
        start_date=date(year=2020, month=2, day=1),
        end_date=date(year=2020, month=3, day=1),
        meetings=[Meeting(eig_1=promo.eigs[0], eig_2=promo.eigs[2])],
    )
    create(weekly_meetings=w_2, promo=promo, redis_server=redis_server)
    create(weekly_meetings=w_1, promo=promo, redis_server=redis_server)

    assert read_all(promo=promo, redis_server=redis_server) == [w_1, w_2]


def test_set_get_current(weekly_meetings, promo, redis_server):
    w_1 = WeeklyMeetings(
        start_date=date(year=2020, month=1, day=1),
        end_date=date(year=2020, month=2, day=1),
        meetings=[Meeting(eig_1=promo.eigs[0], eig_2=promo.eigs[1])],
    )
    w_2 = WeeklyMeetings(
        start_date=date(year=2020, month=2, day=1),
        end_date=date(year=2020, month=3, day=1),
        meetings=[Meeting(eig_1=promo.eigs[0], eig_2=promo.eigs[2])],
    )
    create(weekly_meetings=w_2, promo=promo, redis_server=redis_server)
    create(weekly_meetings=w_1, promo=promo, redis_server=redis_server)
    set_current(w_1, promo=promo, redis_server=redis_server)
    w_1_expected = read_current(promo=promo, redis_server=redis_server)
    assert w_1 == w_1_expected

    set_current(w_2, promo=promo, redis_server=redis_server)
    w_2_expected = read_current(promo=promo, redis_server=redis_server)
    assert w_2 == w_2_expected
