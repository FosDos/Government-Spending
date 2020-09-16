import dash
from dash.dependencies import Input, Output
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash_bootstrap_components as dbc
import requests;
import json;
import os;
df = pd.read_csv('template.csv')
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MINTY])


css_center_text = {"text-align": "center"}
app.layout = html.Div([
    dbc.Row(
        [      
            dbc.Col(html.H1("Press the button to populate the table!"), width = 6, style=css_center_text),
        ],
        justify="center",
    ),

    dbc.Row(
        [
            dbc.Col(html.Div("")),
            dbc.Col(html.Div(dash_table.DataTable(
            style_table={'overflowX': 'auto'},
            id='datatable-interactivity',
            columns=[{"name": i, "id": i, "selectable": False} for i in df.columns],
            data=[],
            sort_action="native",
            page_action="native",
            page_current= 0,
            page_size= 10,
            )), width=10
            ),
            dbc.Col(html.Div("")),
        ],
        no_gutters=True, justify="center",
    ),
    dbc.Row(
        [
         dbc.Col(dbc.Button("Pull Data", id="btn", className="mr-1"), align="center", width = 1, style=css_center_text),
        ],
        justify="center",
    ),
   # html.Button(['Update'],id='btn')  
])

@app.callback(
    [Output("datatable-interactivity","data")],
    [Input("btn", "n_clicks")]
)
def updateTable(n_clicks):
    if n_clicks is None:
        return [df.to_dict('records')];
    URL = "https://api.usaspending.gov/api/v2/references/toptier_agencies/"
    r = requests.get(url = URL)
    data = r.json();
    json_object = json.dumps(data["results"], indent=2)
    file = open("temp.json", "w");
    file.write(json_object);
    file.close();
    panda_object = pd.read_json("temp.json");
    panda_object.to_csv("temp.csv");
    pf = pd.read_csv('temp.csv');
    os.remove('temp.csv');
    os.remove('temp.json');
    return [pf.to_dict('records')];


if __name__ == '__main__':
    app.run_server(debug=False)