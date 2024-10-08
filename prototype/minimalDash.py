from dash import Dash, html, dcc, callback, Output, Input, State
import base64, io
import plotly.express as px
import pandas as pd

app = Dash()

csv_icon = "https://img.icons8.com/ios-filled/50/000000/csv.png"
db_icon = "https://img.icons8.com/ios-filled/50/000000/database.png"
live_icon = "https://img.icons8.com/ios-filled/50/000000/wifi.png"  # Placeholder live data icon

app.layout = html.Div([
    html.H1(children='Data Input Source Selector', style={'textAlign': 'center'}),

    # Input source selector as a single button divided into 3 parts (CSV, Database, Live)
    html.Div([
        html.Button(
            html.Img(src=csv_icon, style={'height': '30px'}),
            id='csv-button', n_clicks=0, className='input-button', 
            style={'flex': '1', 'border': 'none', 'background': 'none', 'border-right': '1px solid black'}
        ),
        html.Button(
            html.Img(src=db_icon, style={'height': '30px'}),
            id='db-button', n_clicks=0, className='input-button', 
            style={'flex': '1', 'border': 'none', 'background': 'none', 'border-right': '1px solid black'}
        ),
        html.Button(
            html.Img(src=live_icon, style={'height': '30px'}),
            id='live-button', n_clicks=0, className='input-button', 
            style={'flex': '1', 'border': 'none', 'background': 'none'}
        )
    ], style={
        'display': 'flex', 'justify-content': 'center', 'align-items': 'center',
        'border': '2px solid black', 'overflow': 'hidden',
        'width': '30%', 'margin': '20px auto'
    }),

    # Hidden div to store persistent data between sessions
    dcc.Store(id='session-data', storage_type='session'),

    # Upload component for CSV file
    dcc.Upload(id='csv-upload', children=html.Button('Upload CSV File', style={'display': 'block', 'margin': '10px 0'}), style={'display': 'none'}),

    # Database input fields (only shown when Database is selected)
    html.Div(id='db-fields', children=[
        html.Label('Table Name:'),
        dcc.Input(id='db-table', type='text', placeholder='Enter Table Name')
    ], style={'display': 'none'}),

    # Placeholder for live data (only shown when "live" is selected)
    html.Div(id='live-data-placeholder', children=[
        html.P('Live data will be integrated here... (This is a placeholder)', style={'font-style': 'italic'})
    ], style={'display': 'none'}),

    # Y-axis selection dropdown
    html.Div(id='y-axis-selection-div', children=[
        html.Label('Select Y-axis Variable:'),
        dcc.Dropdown(id='y-axis-selection', options=[], placeholder='Select a variable', style={'margin-bottom': '10px'}),
    ], style={'display': 'none'}),

    # Graph component
    dcc.Graph(id='graph-content')
])

# Callback to manage input source selection and toggle visibility of components
@callback(
    Output('csv-upload', 'style'),
    Output('db-fields', 'style'),
    Output('live-data-placeholder', 'style'),
    Output('y-axis-selection-div', 'style'),
    Output('session-data', 'data'),
    Input('csv-button', 'n_clicks'),
    Input('db-button', 'n_clicks'),
    Input('live-button', 'n_clicks'),
    State('session-data', 'data')
)
def toggle_input_source(csv_clicks, db_clicks, live_clicks, session_data):
    session_data = session_data or {}
    input_source = 'csv'

    if csv_clicks > db_clicks and csv_clicks > live_clicks:
        input_source = 'csv'
    elif db_clicks > csv_clicks and db_clicks > live_clicks:
        input_source = 'database'
    elif live_clicks > csv_clicks and live_clicks > db_clicks:
        input_source = 'live'

    session_data['input_source'] = input_source
    
    # Show components depending on selected input source
    if input_source == 'csv':
        return {'display': 'block'}, {'display': 'none'}, {'display': 'none'}, {'display': 'block'}, session_data
    elif input_source == 'database':
        return {'display': 'none'}, {'display': 'block'}, {'display': 'none'}, {'display': 'block'}, session_data
    elif input_source == 'live':
        return {'display': 'none'}, {'display': 'none'}, {'display': 'block'}, {'display': 'none'}, session_data

# Callback to update Y-axis dropdown based on uploaded CSV
@callback(
    Output('y-axis-selection', 'options'),
    Output('y-axis-selection', 'value'),
    Input('csv-upload', 'contents')
)
def update_y_axis_options(csv_content):
    if csv_content:
        content_type, content_string = csv_content.split(',')
        decoded = base64.b64decode(content_string)
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        options = [{'label': col, 'value': col} for col in df.columns]
        return options, options[0]['value']  # Set default Y-axis to the first column
    return [], None  # No options if no content

# Callback to update graph based on input source and selected Y-axis
@callback(
    Output('graph-content', 'figure'),
    Input('session-data', 'data'),
    Input('y-axis-selection', 'value'),
    State('db-table', 'value'),
    State('csv-upload', 'contents')
)
def update_graph(session_data, y_axis_var, db_table, csv_content):
    input_source = session_data.get('input_source', 'csv')

    # Handle CSV file upload
    if input_source == 'csv' and csv_content:
        content_type, content_string = csv_content.split(',')
        decoded = base64.b64decode(content_string)
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        
        if 'timestamp' in df.columns and y_axis_var in df.columns:
            fig = px.line(df, x='timestamp', y=y_axis_var, title='Data from CSV')
        else:
            fig = px.line(title='CSV does not contain required columns')
        return fig
    
    # Handle database input (this would require actual database integration)
    elif input_source == 'database' and db_table:
        # Placeholder logic for fetching data from a database
        # df = fetch_data_from_db(db_url, db_table)
        # fig = px.line(df, x='timestamp', y=y_axis_var, title=f'Data from Database ({db_table})')
        fig = px.line(title=f'Data from Database ({db_table})')  # Placeholder
        return fig

    # Handle live data input (placeholder for now)
    elif input_source == 'live':
        fig = px.line(title="Live data will be displayed here.")  # Placeholder figure
        return fig

    # Default figure when no data is available or input source is invalid
    return px.line(title="Select an Input Source and Provide Data")


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
