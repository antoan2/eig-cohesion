from datetime import date

import click

from core.redis_utils import redis_server, load_history
from core.data_loading import load_promo
from core.meetings import WeeklyMeetings
from core.meetings_generation import generate_random_meetings
import core.redis_utils as ru

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    pass

@cli.command()
@click.option('-s', '--start_date', help='Start date of the week.', type=click.DateTime())
@click.option('-e', '--end_date', help='End date of the week', type=click.DateTime())
def more_meetings(start_date, end_date):
    start_date = start_date.date()
    end_date = end_date.date()
    """Simple program that greets NAME for a total of COUNT times."""
    click.echo(f'Hello {start_date} {end_date}!')
    promo = load_promo(4)
    meetings_history = load_history(promo, redis_server)
    meetings = generate_random_meetings(promo=promo, meetings_history=meetings_history)
    created_meetings = WeeklyMeetings(start_date=start_date, end_date=end_date, meetings=meetings)
    ru.add_weekly_meetings(weekly_meetings=created_meetings,promo=promo,  redis_server=redis_server)

if __name__ == '__main__':
    cli()