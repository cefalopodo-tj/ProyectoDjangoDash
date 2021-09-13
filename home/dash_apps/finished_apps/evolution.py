from plotly.offline import plot
#import plotly.graph_objs as go

from dash import dcc
# Deprecated: import dash_html_components as html
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash

import pandas as pd
import numpy as np

import plotly.express as px


lst = [["Manolo",12.23,9],["Jack",15.08,7], ["Lola", 11.14,11]]
df = pd.DataFrame(lst, columns = ['Nombre','Duración media','Encuestas_realizadas'])

lista_nombres=list(df['Nombre'].unique())


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('evolution', external_stylesheets=external_stylesheets)



app.layout = html.Div(
    children=[
    html.H4('Encuestas realizadas por encuestador'),
    dcc.Dropdown(id='my-dropdown', multi=True, #Con multi=True cargamos los diferentes nombres en el gráfico
        options=[{'label':x, 'value':x} for x in sorted(df['Nombre'].unique())],
        value=["Manolo","Jack","Lola"]#lista_nombres #Lista para elegir los nombres que queramos elegir
     ),
    html.Button(id='my-button', n_clicks=0, children="Elige encuestadores"),
    dcc.Graph(id='graph-output', figure={}), 
    html.Div(id='sentence-output', children=["Nombre abajo en la gráfica"], style={}),
    ]
)

@app.callback(
               Output(component_id='graph-output', component_property='figure'),
               [Input(component_id='my-dropdown', component_property='value')],
            )

#Argumento obligatorio. Se tiene que referir a los inputs o a los states de callback (una lista).
#  Ej:2 inputs, 2 argumentos
def update_graph(val_chosen):
    if len(val_chosen) >0:
        print(f"valor del nombre introducido: {val_chosen}")
        dff=df[df['Nombre'].isin(val_chosen)]
        fig=px.pie(dff, values='Encuestas_realizadas', names='Nombre', title='Gráfica por nombre y encuestas realizadas')
        fig.update_traces(textinfo='value+percent').update_layout(title_x=0.5)
        return fig
    elif len(val_chosen) ==0:
        raise dash.exceptions.PreventUpdate

"""
    #Eje abcisas
    #x1=[1,2,3,4]
    #Eje ordenadas
    #y1=[30,35,25,45]
    #Configuramos el rastro
    graph=go.Scatter(
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
"""    

# IMPORTANTE IMPORTAR EN urls.py!!!!!