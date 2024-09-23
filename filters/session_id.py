import dash_mantine_components as dmc 
from dash import dcc, callback, Output, Input, State, html
from db.mongodb import get_db

def SessionIdFilter():
    return dmc.Container(
        children=[
            dmc.Select(
                allowDeselect=False,
                label="Session ID",
                id="session-id-filter",
                sx={"marginBottom": "1rem"},
                data=[]
            ), 
            dcc.Store(id="session-id", storage_type="session", data=0)
        ]
    )

@callback(
    Output("session-id", "data"),
    Input("session-id-filter", "value")
)
def update_session_id(value):
    return value

@callback(Output("session-id-filter", "data"),  Input("session-id-offline", "data"),  Input("url", "href"))
def update_session_id_values(data, _url):
    try:
        db = get_db()
        collection = db["realtime_metrics"]
        session_ids = collection.distinct("metadata.session_id")
        return sorted(session_ids, key=int)
    except:
        # returns offline session_ids if unable to connect to DFR Mongo cluster
        data_string = [str(ids) for ids in data] 
        return sorted(data_string, key=int)
    