# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import json
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash.dependencies import Input, Output, State, MATCH, ALL
from core.data_loading import load_promo
from db import redis_server
from crud.weekly_meetings import (
    read_all_except_current,
    read_current,
    read_current_key,
    set_meeting_done,
    set_meeting_not_done,
    read,
)
from display.weekly_meetings_card import get_weekly_meetings_card
from models import weekly_meetings

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
app.title = "Eig Cohésionneur"

server = app.server

PROMO = load_promo(promo_number=4)
REDIS_SERVER = redis_server


def get_current_weekly_meetings_card() -> html.Div:
    current_weekly_meetings = read_current(PROMO, REDIS_SERVER)
    current_weekly_meetings_card = get_weekly_meetings_card(
        current_weekly_meetings, current=True
    )
    return current_weekly_meetings_card


def get_previous_weekly_meetings_cards():
    list_weekly_meetings = read_all_except_current(PROMO, REDIS_SERVER)
    return [
        get_weekly_meetings_card(weekly_meetings)
        for weekly_meetings in list_weekly_meetings
    ]


title = html.Div(
    [
        dbc.Row(
            [html.H1("EIG Cohésionneur")],
            justify="center",
            align="center",
            className="mt-5",
        ),
        dbc.Row(
            [
                html.H5(
                    "Le plus on se parle, le plus on se connait",
                    style={"font-style": "italic"},
                )
            ],
            justify="center",
            align="center",
            className="mb-5",
        ),
    ]
)

app.layout = html.Div(
    children=[
        dcc.Location(id="url", refresh=False),
        title,
        html.Div(id="current_weekly_meetings"),
        html.Div(id="previous_weekly_meetings"),
    ]
)


@app.callback(
    Output("current_weekly_meetings", "children"),
    Input({"type": "checklist", "index": ALL}, "value"),
)
def display_current_weekly_meetings(values):
    weekly_meetings_key = read_current_key(PROMO, REDIS_SERVER)
    ctx = dash.callback_context
    if ctx.triggered[0]["prop_id"] != ".":
        meeting_hash = json.loads(ctx.triggered[0]["prop_id"].split(".")[0])["index"]
        value = ctx.triggered[0]["value"]
        if value == ["done"]:
            set_meeting_done(
                meeting_hash=meeting_hash,
                weekly_meetings_key=weekly_meetings_key,
                redis_server=REDIS_SERVER,
            )
        else:
            set_meeting_not_done(
                meeting_hash=meeting_hash,
                weekly_meetings_key=weekly_meetings_key,
                redis_server=REDIS_SERVER,
            )
    weekly_meetings = read(weekly_meetings_key, PROMO, REDIS_SERVER)
    weekly_meetings_card = get_weekly_meetings_card(weekly_meetings, current=True)
    return weekly_meetings_card


@app.callback(Output("previous_weekly_meetings", "children"), Input("url", "pathname"))
def display_previous_weekly_meetings(pathname):
    return get_previous_weekly_meetings_cards()


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0")