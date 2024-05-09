import dash
from dash import dcc
from dash import html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True

df = pd.read_csv("./results/loading.csv").drop(["Unnamed: 0"], axis=1)
edges_df = pd.read_csv("./results/loading_edges.csv", index_col=0)

app.layout = html.Div(
    [
        html.H1("ArangoDB Analysis Visualization"),
        dcc.Tabs(
            id="tabs",
            value="tab-centralized",
            children=[
                dcc.Tab(
                    label="Centralized Version", value="tab-centralized"
                ),  # definition of the tabs
                dcc.Tab(label="Distribuited Version", value="tab-distribuited"),
            ],
        ),
        html.Div(id="tabs-content-example"),
    ]
)


@app.callback(
    Output("tabs-content-example", "children"),  # callback on tab object
    [Input("tabs", "value")],
)
def render_content(tab):
    if tab == "tab-centralized":
        return html.Div(
            [
                html.H2("Centralized Version"),
                dcc.Dropdown(
                    id="column-selector",
                    options=df.columns.to_list(),  # Mostra tutte le colonne
                    value=df.columns[0],  # Preseleziona la prima colonna
                    clearable=False,
                ),
                # Aggiungi il grafico
                dcc.Graph(id="graph"),
                html.H2("Edges"),
                dcc.Dropdown(
                    id="edges-selector",
                    options=edges_df.columns.to_list(),
                    value=edges_df.columns[0],
                    clearable=False,
                ),
                dcc.Graph(id="edges-graph"),
            ]
        )
    elif tab == "tab-distribuited":
        return html.Div(
            [
                html.H2("Distribuited Version"),
            ]
        )


@app.callback(Output("graph", "figure"), [Input("column-selector", "value")])
def update_graph(selected_column):
    trace = go.Scatter(
        x=['Centralized', "Distribuited"],
        y=df[selected_column],
        error_y=dict(type="data", array=[df[selected_column].std()], visible=True),
        name=selected_column,
        mode="markers",
    )
    layout = go.Layout(
        title=f"Grafico di {selected_column}",
        xaxis=dict(title="Versione"),
        yaxis=dict(title="Tempo impiegato (secondi)"),
    )
    return {"data": [trace], "layout": layout}


@app.callback(Output("edges-graph", "figure"), [Input("edges-selector", "value")])
def update_graph(selected_column):
    trace = go.Scatter(
        x=edges_df.index, y=edges_df[selected_column], name=selected_column
    )
    layout = go.Layout(
        title=f"Grafico di {selected_column}",
        xaxis=dict(title="Numero di archi caricati"),
        yaxis=dict(title="Tempo impiegato (secondi)"),
    )
    return {"data": [trace], "layout": layout}


if __name__ == "__main__":
    app.run_server(debug=True)
