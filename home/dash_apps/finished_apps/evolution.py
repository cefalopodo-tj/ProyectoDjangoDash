from plotly.offline import plot
#import plotly.graph_objs as go

from dash import dcc
# Deprecated: import dash_html_components as html
from dash import html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash

import pandas as pd
import numpy as np

import plotly.express as px


lst = [["Manolo",12.23,9],["Jack",15.08,7], ["Lola", 11.14,11], ['Jaime', 13.45, 10]]
df = pd.DataFrame(lst, columns = ['Nombre','Duración media','Encuestas_realizadas'])

lista_nombres=list(df['Nombre'].unique())


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('evolution', external_stylesheets=external_stylesheets)



app.layout = html.Div(
    children=[
    html.H4('Encuestas realizadas por encuestador'),
    dcc.Dropdown(id='my-dropdown', multi=True, #Con multi=True cargamos los diferentes nombres en el gráfico
        options=[{'label':x, 'value':x} for x in sorted(df['Nombre'].unique())],
        value=lista_nombres  #Lista para elegir los nombres que queramos elegir
     ),
    html.Button(id='my-button', n_clicks=0, children="Elige encuestadores"),
    dcc.Graph(id='graph-output', figure={}), 
    html.Div(id='sentence-output', children=["Nombre abajo en la gráfica"], style={}),
    ]
)

@app.callback(
               Output(component_id='graph-output', component_property='figure'),
               [Input(component_id='my-button', component_property='n_clicks')],
               [State(component_id= 'my-dropdown', component_property='value')],
               prevent_initial_call=False # Lo usamos para que cuando tengamos a nadie elegido que el gráfico no se actualice Lo lanzamos en la función de abajo
            )

#Argumento obligatorio. Se tiene que referir a los inputs o a los states de callback (una lista).
#  Ej:2 inputs, 2 argumentos
def update_graph(n, val_chosen):
    if len(val_chosen) >0:
        print(f"valor del nombre introducido: {val_chosen}")
        dff=df[df['Nombre'].isin(val_chosen)]
        fig=px.pie(dff, 
            values='Encuestas_realizadas', 
            names='Nombre',
            title='Gráfica por nombre y encuestas realizadas',
            hole=.2,)
        fig.update_traces(textinfo='value+percent').update_layout(title_x=0.5)
        return fig
    elif len(val_chosen) ==0:
        raise dash.exceptions.PreventUpdate  # Lo usamos para que cuando tengamos a nadie elegido que el gráfico no se actualice Lo lanzamos en la función de abajo



# IMPORTANTE IMPORTAR EN urls.py!!!!!