from numpy import int64
from dash import Dash, dcc, html, Output, Input
import plotly.express as px
import pandas as pd
import json

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

    fig = px.choropleth(filtered_df, locations=filtered_df.name, geojson=filtered_df.geometry, color='Avg Life Expectancy',
                        color_continuous_scale="Viridis",
                        range_color=(0, 12),
                        labels={'Avg Life Expectancy': 'Life Expectancy'}
                        )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
