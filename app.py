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
df = pd.DataFrame(columns = ["agency_id","toptier_code","abbreviation","agency_name","congressional_justification_url","active_fy","active_fq","outlay_amount","obligated_amount","budget_authority_amount","current_total_budget_authority_amount","percentage_of_total_budget_authority"])
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
            columns=[{"name": i, "id": i} for i in df.columns],
            data=[],
            sort_action="native",
            page_action="native",
            page_current= 0,
            page_size= 20,
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
    jo = pd.DataFrame.from_dict(data["results"]);
    return [jo.to_dict('records')];


if __name__ == '__main__':
    app.run_server(debug=False)