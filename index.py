import glob

import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import io
import base64

app = dash.Dash()

app.layout = html.Div(
    [
        dcc.Upload(
            id="upload-data",
            children=html.Div(["Drag and Drop or ", html.A("Select Files")]),
            style={
                "width": "25%",
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "margin": "auto",
            },
            multiple=False,
        ),
        html.Div(id="output-data-upload"),
        dcc.Graph(
            id="graph", style={"width": "700px", "height": "700px", "margin": "auto"}
        ),
    ],
    style={"width": "100%", "height": "100%"},
)


@app.callback(
    Output("graph", "figure"),
    [Input("upload-data", "contents")],
    [State("upload-data", "filename")],
)
def update_output(contents_input, filename):
    if any([i is None for i in [contents_input, filename]]):
        raise PreventUpdate
    if not filename.endswith(".csv"):
        raise PreventUpdate

    contents_string = contents_input.split(",")[1]
    decoded = base64.b64decode(contents_string)
    contents = io.StringIO(decoded.decode("utf-8"))

    df = pd.read_csv(contents, index_col=0)

    df.Head_Pos_x += 0.5
    df.Head_Pos_y += 0.5
    df.Food_Pos_x += 0.5
    df.Food_Pos_y += 0.5

    snake_x = []
    snake_y = []

    for i, row in enumerate(df.itertuples()):
        if i:
            this_x = snake_x[-1][-(row.Snake_Length) + 1: ]
            this_y = snake_y[-1][-(row.Snake_Length) + 1: ]
        else:
            this_x = [row.Tail_Pos_x + 0.5]
            this_y = [row.Tail_Pos_y + 0.5]
        this_x.append(row.Head_Pos_x)
        this_y.append(row.Head_Pos_y)

        snake_x.append(this_x)
        snake_y.append(this_y)

    x_range = [0, df.Grid_Size.iloc[0]]
    y_range = [0, df.Grid_Size.iloc[0]]

    frames = [
        go.Frame(
            data=[
                go.Scatter(
                    x=snake_x[i],
                    y=snake_y[i],
                    mode="lines",
                    line={"width": 20},
                    name="Snake Body",
                ),
                go.Scatter(
                    x=[row.Head_Pos_x],
                    y=[row.Head_Pos_y],
                    mode="markers",
                    marker={"size": 20},
                    name="Snake Head",
                ),
                go.Scatter(
                    x=[row.Food_Pos_x],
                    y=[row.Food_Pos_y],
                    mode="markers",
                    marker={"size": 20, "symbol": "star"},
                    name="Food",
                ),
            ],
            layout={"title": f"Score : {int(row.Snake_Length):d}"},
        )
        for i, row in enumerate(df.itertuples())
    ]

    return go.Figure(
        data=frames[0].data[:],
        layout={
            "xaxis": {
                "range": x_range,
                "tick0": 0,
                "dtick": 1,
                "showticklabels": False,
            },
            "yaxis": {
                "range": y_range,
                
                "tick0": 0,
                "dtick": 1,
                "showticklabels": False,
            },
            "updatemenus": [
                dict(
                    type="buttons",
                    buttons=[
                        dict(
                            label="Play",
                            method="animate",
                            args=[
                                None,
                                {
                                    "frame": {"duration": 125, "redraw": True},
                                    "fromcurrent": True,
                                    "transition": {
                                        "duration": 0,
                                        "easing": "quadratic-in-out",
                                    },
                                },
                            ],
                        )
                    ],
                )
            ],
        },
        frames=frames,
    )


if __name__ == "__main__":
    app.run_server(host="localhost")
