from dash import Dash, html, dcc, callback, Output, Input, State
import base64, io
import plotly.express as px
import pandas as pd

app = Dash()

csv_icon = "https://img.icons8.com/ios-filled/50/000000/csv.png"
db_icon = "https://img.icons8.com/ios-filled/50/000000/database.png"

app.layout = html.Div([
    html.H1(children='Data Input Source Selector', style={'textAlign': 'center'}),

    # Input source selection with a label and picture
    html.Div([
        html.Label('Select Input Source:', style={'font-weight': 'bold'}),
        dcc.Dropdown(
            options=[
                {'label': html.Div(['CSV File', html.Img(src=csv_icon, style={'height': '25px', 'margin-left': '10px'})], style={'display': 'flex', 'align-items': 'center'}), 'value': 'csv'},
                {'label': html.Div(['Database', html.Img(src=db_icon, style={'height': '25px', 'margin-left': '10px'})], style={'display': 'flex', 'align-items': 'center'}), 'value': 'database'}
            ],
            value='csv',  # Default selection
            id='input-source-selection'
        )
    ], style={'margin': '20px 0'}),

    # Hidden div to store persistent data between sessions
    dcc.Store(id='session-data', storage_type='session'),

    # Upload component 
    dcc.Upload(id='csv-upload', children=html.Button('Upload CSV File', style={'display': 'block', 'margin': '10px 0'}), style={'display': 'none'}),

    # Database input fields (only shown when Database is selected)
    html.Div(id='db-fields', children=[
        html.Label('Database URL:'),
        dcc.Input(id='db-url', type='text', placeholder='Enter DB URL', style={'margin-bottom': '10px'}),
        html.Label('Table Name:'),
        dcc.Input(id='db-table', type='text', placeholder='Enter Table Name')
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
    Output('y-axis-selection-div', 'style'),
    Output('session-data', 'data'),
    Input('input-source-selection', 'value'),
    State('session-data', 'data')
)
def toggle_input_source(input_source, session_data):
    # Update session data with the selected source
    session_data = session_data or {}
    session_data['input_source'] = input_source
    
    # Show upload field for CSV, or DB fields for database
    if input_source == 'csv':
        return {'display': 'block'}, {'display': 'none'}, {'display': 'block'}, session_data
    elif input_source == 'database':
        return {'display': 'none'}, {'display': 'block'}, {'display': 'none'}, session_data

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
    State('db-url', 'value'),
    State('db-table', 'value'),
    State('csv-upload', 'contents')
)
def update_graph(session_data, y_axis_var, db_url, db_table, csv_content):
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
    elif input_source == 'database' and db_url and db_table:
        # Placeholder logic for fetching data from a database
        # df = fetch_data_from_db(db_url, db_table)
        # fig = px.line(df, x='timestamp', y=y_axis_var, title=f'Data from Database ({db_table})')
        fig = px.line(title=f'Data from Database ({db_table})')  # Placeholder
        return fig
    
    # Default figure when no data is available or input source is invalid
    return px.line(title="Select an Input Source and Provide Data")


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
