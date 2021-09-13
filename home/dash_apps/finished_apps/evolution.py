from plotly.offline import plot
#import plotly.graph_objs as go

from dash import dcc
# Deprecated: import dash_html_components as html
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('evolution', external_stylesheets=external_stylesheets)


app.layout = html.Div([
    html.H4('Evolución de teléfonos por encuesta'),
    dcc.Graph(id='graph', animate=True, style={"backgroundColor": "#1a2d46", 'color': '#ffffff'}),
    dcc.Slider(
        id='slider-updatemode',
        marks={i: '{}'.format(i) for i in range(20)},
        max=20,
        value=2,
        step=1,
        updatemode='drag',
    ), 
])

@app.callback(
               Output('graph', 'figure'),
               [Input(component_id='slider-updatemode', component_property='value')]
            )


def scatter(value):
    #Eje abcisas
    x1=[1,2,3,4]
    #Eje ordenadas
    y1=[30,35,25,45]
    #Configuramos el rastro
    graph2=go.Scatter(
        x=x1,
        y=y1
    )
    #Configuramos el layout
    layout2=go.layout(
        paper_bgcolor='#27293d',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(range=[min(x1), max(x1)]),
        yaxis= dict(range= [min(y1), max(y1)])
    )
    #Creamos el dibujo
    #fig = go.Figure(data=[trace], layout=layout)
    #Creamos el plot
    #plot_div= plot(fig, output_type ='div', include_plotlyjs=False)
    return {'data': [graph2], 'layout': layout2}
    

# IMPORTANTE IMPORTAR EN urls.py!!!!!