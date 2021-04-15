from datetime import date, timedelta

import click

from db import redis_server

# from core.redis_utils import load_history
from core.data_loading import load_promo
from models import WeeklyMeetings, weekly_meetings
from crud.meeting_history import read_history
import crud.weekly_meetings as crud_weekly_meetings
import crud.meeting as crud_meeting
from core.meetings_generation import generate_random_meetings

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    pass


@cli.command()
@click.option(
    "-s",
    "--start_date",
    help="Start date of the week.",
    type=click.DateTime(),
    required=True,
)
def new_week(start_date):
    """
    Create a new week of meetings !!
    """
    start_date = start_date.date()
    end_date = start_date + timedelta(days=7)
    click.echo(f"Hello {start_date} {end_date}!")
    promo = load_promo(4)
    meetings_history = read_history(promo, redis_server)
    meetings = generate_random_meetings(promo=promo, meetings_history=meetings_history)
    created_weekly_meetings = WeeklyMeetings(
        start_date=start_date, end_date=end_date, meetings=meetings
    )
    crud_weekly_meetings.create(
        weekly_meetings=created_weekly_meetings, promo=promo, redis_server=redis_server
    )
    crud_weekly_meetings.set_current(
        weekly_meetings=created_weekly_meetings, promo=promo, redis_server=redis_server
    )


@cli.command()
def next_week():
    """Simple program that greets NAME for a total of COUNT times."""
    promo = load_promo(4)
    current_weekly_meetings = crud_weekly_meetings.read_current(
        promo=promo, redis_server=redis_server
    )
    start_date = current_weekly_meetings.end_date
    end_date = start_date + timedelta(days=7)

    for meeting in current_weekly_meetings:
        print("Current week: ", meeting)
        if meeting.done:
            crud_meeting.push_meeting_to_history(
                meeting=meeting, promo=promo, redis_server=redis_server
            )
    meetings_history = read_history(promo, redis_server)
    meetings = generate_random_meetings(promo=promo, meetings_history=meetings_history)
    created_weekly_meetings = WeeklyMeetings(
        start_date=start_date, end_date=end_date, meetings=meetings
    )
    crud_weekly_meetings.create(
        weekly_meetings=created_weekly_meetings, promo=promo, redis_server=redis_server
    )
    crud_weekly_meetings.set_current(
        weekly_meetings=created_weekly_meetings, promo=promo, redis_server=redis_server
    )

    # click.echo(f"Hello {start_date} {end_date}!")

    # start_date = start_date.date()
    # end_date = end_date.date()
    # end_date = start_date + timedelta(days=7)
    # meetings_history = read_history(promo, redis_server)
    # meetings = generate_random_meetings(promo=promo, meetings_history=meetings_history)
    # created_weekly_meetings = WeeklyMeetings(
    #     start_date=start_date, end_date=end_date, meetings=meetings
    # )
    # crud_weekly_meetings.create(
    #     weekly_meetings=created_weekly_meetings, promo=promo, redis_server=redis_server
    # )
    # crud_weekly_meetings.set_current(weekly_meetings=created_weekly_meetings)


if __name__ == "__main__":
    cli()