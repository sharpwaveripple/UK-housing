import itertools

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
import statsmodels.api as sm


def read_data(fpath):
    df = pd.read_excel(fpath, skiprows=2)
    z = itertools.product(regions, m)
    colnames = ["quarter"] + ["_".join(map(str, x)) for x in z]
    df.columns = colnames
    qs = [f"{x.split()[1]}-{x.split()[0]}" for x in df["quarter"]]
    df["quarter"] = pd.PeriodIndex(qs, freq="Q").to_timestamp()
    return df


regions = [
    "north",
    "yorks_hside",
    "north_west",
    "east_mids",
    "west_mids",
    "east_anglia",
    "outer_s_east",
    "outer_met",
    "london",
    "south_west",
    "wales",
    "scotland",
    "n_ireland",
    "uk",
]
m = ["price", "index"]

# sm.tsa.x13.x13_arima_analysis()

fpath = "test.xls"
df = read_data(fpath)
all_regions = [x for x in list(df) if "price" in x]
df = pd.melt(df, "quarter")

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]


app = dash.Dash(__name__)

app.layout = html.Div(
    [
        dcc.Checklist(
            id="checklist",
            options=[{"label": x, "value": x} for x in all_regions],
            value=["uk_price"],
            labelStyle={"display": "inline-block"},
        ),
        dcc.Graph(id="line-chart"),
    ]
)


@app.callback(Output("line-chart", "figure"), [Input("checklist", "value")])
def update_line_chart(continents):
    mask = df.variable.isin(continents)
    fig = px.line(df[mask], x="quarter", y="value", color="variable")
    fig.update_xaxes(rangeslider_visible=True)
    return fig


if __name__ == "__main__":
    app.run_server(host='127.0.0.1', port='8050', debug=True)
