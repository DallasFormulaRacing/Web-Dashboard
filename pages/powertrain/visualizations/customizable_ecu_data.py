from dash import html, dcc, callback
import dash
import dash_mantine_components as dmc
from dash.dependencies import Input, Output
import pandas as pd
from dash_iconify import DashIconify
import plotly.express as px
# from db.mongodb import get_data
PAGE = "powertrain"
VIZ_ID = "customizable_graph"

ID = f"{PAGE}-{VIZ_ID}"

try:
    df = pd.read_csv('./ecu_data.csv', header="infer")
except:
    df = pd.DataFrame()

y_axis_options = [{'label': col, 'value': col} for col in df.columns if col != "timestamp"]

gc_customizable_graph = dmc.Card(
    id="customizable-ecu-data",
    children=[
        dmc.CardSection(
            [
                dmc.Group(
                    children=[
                        dmc.Text("RPM vs Map vs Lambda", weight=500, id="graph-title"),
                        dmc.ActionIcon(
                            DashIconify(icon="carbon:overflow-menu-horizontal"),
                            color="gray",
                            variant="transparent",
                        ),
                    ],
                    position="apart",
                ),
                dmc.Text(
                    children=["This graph can be configured for any value of the engine over time. "],
                    mt="sm",
                    color="dimmed",
                    size="sm",
                ),
            ],
            inheritPadding=True,
            py="xs",
            withBorder=True,
        ),
        dmc.CardSection(
            [
            dmc.MultiSelect(
                    id="y-axis-dropdown",
                    data=y_axis_options,
                    value=["RPM"],
                    style={"width": "50%"}
                ),
            dcc.Loading(
                dcc.Graph(id=ID),
            )
            ]
        ),
    ],
    withBorder=True,
    shadow="sm",
    radius="md",
    p="xs",
    m="xs",
    bg="black",
    style={"width": "100%"},
)

# callback to dynamically change y-axis
@callback(
    [Output("graph-title", "children"),
     Output(ID, "figure")],
    [Input("y-axis-dropdown", "value")]
)
def customizable_graph(y_axis_variable):
    graph_title = f"{', '.join(y_axis_variable)} vs Time (sec)"

    fig = px.line(
        df,
        x="timestamp",
        y=y_axis_variable,
        labels={"timestamp": "Time"}
    )
    fig.update_layout(title=graph_title)
    return graph_title, fig