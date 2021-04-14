import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from core.meetings import WeeklyMeetings, Meeting


def get_weekly_meetings_card(weekly_meeting: WeeklyMeetings):
    # checklist_meetings = get_checklist(weekly_meeting["meetings"])
    progress = weekly_meeting.get_progres()
    color = 'danger'
    if progress > 25 and progress < 75:
        color = 'warning'
    elif progress >= 75:
        color = 'success'
    checklists = [get_checklist(meeting) for meeting in weekly_meeting]
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
                    dbc.Progress(
                        value=progress,
                        color=color,
                        id="progress-bar",
                    ),
                    # checklist_meetings,
                    dbc.Row(
                        [
                            dbc.Col(checklist_col_1),
                            dbc.Col(checklist_col_2),
                        ],
                        className='m-4'
                    ),
                ]
            ),
        ],
        className="m-5",
    )
    return card


def get_checklist(meeting: Meeting):
    if meeting.done:
        value = ['done']
    else:
        value = []
    return dbc.Checklist(
        options=[{"label": str(meeting), "value": 'done'}],
        value=value,
        id={'type':'checklist', 'index': f'{meeting.get_hash()}'},
        className="m-2",
    )