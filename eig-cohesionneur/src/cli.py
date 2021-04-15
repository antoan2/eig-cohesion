from datetime import date, timedelta

import click

from db import redis_server

# from core.redis_utils import load_history
from core.data_loading import load_promo
from models import WeeklyMeetings
from crud.meeting_history import read_history
from core.meetings_generation import generate_random_meetings
import core.redis_utils as ru

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    pass


@cli.command()
@click.option(
    "-s", "--start_date", help="Start date of the week.", type=click.DateTime()
)
def next_week(start_date, end_date):
    start_date = start_date.date()
    end_date = end_date.date()
    """Simple program that greets NAME for a total of COUNT times."""
    click.echo(f"Hello {start_date} {end_date}!")
    promo = load_promo(4)
    meetings_history = read_history(promo, redis_server)
    meetings = generate_random_meetings(promo=promo, meetings_history=meetings_history)
    created_meetings = WeeklyMeetings(
        start_date=start_date, end_date=end_date, meetings=meetings
    )
    ru.add_weekly_meetings(
        weekly_meetings=created_meetings, promo=promo, redis_server=redis_server
    )


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
    for meeting in meetings_history:
        print(meetings_history)

    meetings = generate_random_meetings(promo=promo, meetings_history=meetings_history)
    print(meetings)
    # created_metings = WeeklyMeetings(
    #     start_date=start_date, end_date=end_date, meetings=meetings
    # )
    # ru.add_weekly_meetings(
    #     weekly_meetings=created_meetings, promo=promo, redis_server=redis_server
    # )


if __name__ == "__main__":
    cli()