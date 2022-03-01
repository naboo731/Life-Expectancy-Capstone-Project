from numpy import int64
from dash import Dash, dcc, html, Output, Input
import plotly.express as px
import pandas as pd
import json
import plotly.graph_objs as go

df = pd.read_csv('format_totalpop.csv')
df['year'] = df['year'].astype('int64')


app = Dash(__name__)


app.layout = html.Div(children=[
    html.H1(children='Total Population Life Expectancy Change Over Years'),
    html.Div([
        dcc.Graph(id='graph-with-slider'),
        dcc.Slider(
            df['year'].min(),
            df['year'].max(),
            step=None,
            value=df['year'].min(),
            marks={str(year): str(year) for year in df['year'].unique()},
            id='year_slider'
        )
    ])
])


@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('year_slider', 'value'))
def update_figure(year_slider):
    filtered_df = df[df.year == year_slider].copy()

    data = dict(type='choropleth',
                locations=filtered_df['name'],
                locationmode='country names',
                text=filtered_df['name'],
                z=filtered_df['Avg Life Expectancy'],
                )
    layout = dict(geo=dict(scope='world',
                           showlakes=False)
                  )

    choromap = go.Figure(data=[data], layout=layout)
    return choromap


if __name__ == '__main__':
    app.run_server(debug=True)
