import dash
from dash import html, dcc
import dash_mantine_components as dmc
from utils.analytics_page import make_components
from .visualizations.csv_upload import upload
from .visualizations.test_upload import test_graph
dash.register_page(__name__, path="/fileupload", name="FileUpload")

graphs = {
    "File Upload": {
        "Upload Button": upload,
        "Demo Graph": test_graph
    }
}

layout = make_components(graphs)