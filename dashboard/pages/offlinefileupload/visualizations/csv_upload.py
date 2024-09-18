from dash import html, dcc, Input, Output, State
import dash
import dash_mantine_components as dmc
from dash import callback
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import timeit

import base64
import datetime
import io

PAGE = "fileupload"
VIZ_ID = "csv_file_upload_area"

upload = dmc.Card([
    html.H3(
                    "csv file upload",
                    className="card-title",
                    style={"textAlign": "center"},
                ),
    dcc.Upload(
        id='csv-file-upload',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
        },
        multiple=True
    ),
    html.Div(id='offline-data')
])


def parse_contents(contents):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    df = pd.read_csv(
        io.StringIO(decoded.decode('utf-8')))
    return df


@callback(Output("is-offline", "data"), Input("offline-data", "data"))
def update_offline_status(_offline_data):
    if PAGE == "fileupload":
        return True

@callback(Output("session-id-current", "data"), State("session-id-current", "data"), Input("offline-data", "data"))
def update_offline_sessions_count(_session_id_current, _offline_data):
    #print(_offline_data)
    return _session_id_current + 1


@callback(Output("session-id-offline", "data"), State("session-id-offline", "data"), Input("offline-data", "data"))
def update_offline_sessions(_session_id_offline, _session_data):
    # prevents cyclic dependencies
    _session_id_offline.append(_session_id_offline[len(_session_id_offline) -1 ]+1)
    #lengthDataframeList = 0 
    #if _session_data != None:
    #    lengthDataframeList = (len(_session_data) -1 )
    #if _session_id_offline == None:
    #    _session_id_offline = [-1]

    #_session_id_offline = _session_id_offline.append([range(_session_id_offline[len(_session_id_offline) -1 ], lengthDataframeList )])
    #print(_session_id_offline)

    return _session_id_offline


@callback(Output('offline-data', 'data'), State('offline-data', 'data'),
              Input('csv-file-upload', 'contents'))
def update_output(_offline_data, list_of_contents):
    #print('data')
    #print(_offline_data)

    if list_of_contents is not None:
        children = [
            parse_contents(c).to_json(date_format="iso", orient="split") for c in
            list_of_contents]
        #print('data')
        #print(children)
        if _offline_data != None:
            children = children + _offline_data

        return children