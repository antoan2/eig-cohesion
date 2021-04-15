from logging import disable
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from models import WeeklyMeetings, Meeting


def get_checklist(meeting: Meeting, disabled: bool) -> dbc.Checklist:
    if meeting.done:
        value = ["done"]
    else:
        value = []
    if disabled:
        return dbc.Checklist(
            options=[{"label": str(meeting), "value": "done", "disabled": True}],
            value=value,
            className="m-2",
        )
    else:
        return dbc.Checklist(
            options=[{"label": str(meeting), "value": "done", "disabled": False}],
            value=value,
            id={"type": "checklist", "index": f"{meeting.get_hash()}"},
            className="m-2",
        )


def get_progress_bar_color(progress: float) -> str:
    color = "danger"
    if progress > 25 and progress < 75:
        color = "warning"
    elif progress >= 75:
        color = "success"
    return color


def get_weekly_meetings_card(weekly_meeting: WeeklyMeetings, current: bool = False):
    progress = weekly_meeting.get_progres()
    progress_bar_color = get_progress_bar_color(progress=progress)

    if current == True:
        checklist_disabled = False
        id_progress_bar = "progress-bar"
        progress_bar = dbc.Progress(
            value=progress,
            color=progress_bar_color,
            id=id_progress_bar,
        )
    else:
        checklist_disabled = True
        progress_bar = dbc.Progress(
            value=progress,
            color=progress_bar_color,
        )

    checklists = [
        get_checklist(meeting=meeting, disabled=checklist_disabled)
        for meeting in weekly_meeting
    ]
    len_column = int(len(checklists) / 2)
    checklist_col_1 = checklists[:len_column]
    checklist_col_2 = checklists[len_column:]

    card = dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H4(
                        "Semaine du {} au {}".format(
                            weekly_meeting.start_date, weekly_meeting.end_date
                        ),
                        className="card-title",
                    ),
                    progress_bar,
                    # checklist_meetings,
                    dbc.Row(
                        [
                            dbc.Col(checklist_col_1),
                            dbc.Col(checklist_col_2),
                        ],
                        className="m-4",
                    ),
                ]
            ),
        ],
        className="m-5",
    )
    return card
