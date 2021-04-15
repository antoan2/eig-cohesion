# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import logging
import os

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
    WEEKLY_MEETINGS_KEY_PREFIX,
    read_current,
    read_current_key,
    set_meeting_done,
    set_meeting_not_done,
    read,
)
from display.weekly_meetings_card import get_weekly_meetings_card

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
app.title = "Eig Cohésionneur"

server = app.server

PROMO = load_promo(promo_number=4)
REDIS_SERVER = redis_server
WEEKLY_MEETINGS_IDS = read_current_key(PROMO, REDIS_SERVER)


def get_div_weekly_meetings_card():
    current_weekly_meetings = read_current(PROMO, REDIS_SERVER)
    current_weekly_meetings_card = get_weekly_meetings_card(current_weekly_meetings)
    return html.Div(children=current_weekly_meetings_card, id=WEEKLY_MEETINGS_IDS)


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

app.layout = html.Div(children=[title, get_div_weekly_meetings_card()])


@app.callback(
    Output(WEEKLY_MEETINGS_IDS, "children"),
    Input({"type": "checklist", "index": ALL}, "value"),
)
def display_output(values):
    ctx = dash.callback_context
    if ctx.triggered[0]["prop_id"] != ".":
        meeting_hash = json.loads(ctx.triggered[0]["prop_id"].split(".")[0])["index"]
        value = ctx.triggered[0]["value"]
        if value == ["done"]:
            set_meeting_done(
                meeting_hash=meeting_hash,
                weekly_meetings_key=WEEKLY_MEETINGS_IDS,
                redis_server=REDIS_SERVER,
            )
        else:
            set_meeting_not_done(
                meeting_hash=meeting_hash,
                weekly_meetings_key=WEEKLY_MEETINGS_IDS,
                redis_server=REDIS_SERVER,
            )
    weekly_meetings = read(WEEKLY_MEETINGS_IDS, PROMO, REDIS_SERVER)
    weekly_meetings_card = get_weekly_meetings_card(weekly_meetings)
    return weekly_meetings_card


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0")