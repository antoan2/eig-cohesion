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
from models.meeting import Meeting

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
@click.option(
    "-p",
    "--promo_number",
    help="The number of the promo",
    type=int,
    default=4,
)
def new_week(start_date, promo_number):
    """
    Create a new week of meetings !!
    """
    start_date = start_date.date()
    end_date = start_date + timedelta(days=7)
    click.echo(f"Hello {start_date} {end_date}!")
    promo = load_promo(promo_number=promo_number)
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
@click.option(
    "-p",
    "--promo_number",
    help="The number of the promo",
    type=int,
    default=4,
)
def next_week(promo_number):
    """Simple program that greets NAME for a total of COUNT times."""
    promo = load_promo(promo_number=promo_number)
    current_weekly_meetings = crud_weekly_meetings.read_current(
        promo=promo, redis_server=redis_server
    )
    start_date = current_weekly_meetings.end_date
    end_date = start_date + timedelta(days=7)
    if not click.confirm(
        f"Are you sure you want to create a full week (from {start_date} to {end_date}) of new meetings ?"
    ):
        return

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


@cli.command()
def flush_all():
    if click.confirm("Are you sure you want to flush all data from redis ?"):
        redis_server.flushall()




if __name__ == "__main__":
    cli()