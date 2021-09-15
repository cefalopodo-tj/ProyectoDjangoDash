import pandas as pd
import plotly
import plotly.express as px

import dash
#Deprecated:
#import dash_table
from dash import dash_table
from dash import dcc
from dash import html
from django_plotly_dash import DjangoDash
from dash.dependencies import Input, Output

#Gráfico interactivo donde lo que vayamos seleccionando en la tabla se incluirá en los gráficos creados abajo

#Dataframe ejemplo
lst = [["05/04/2021","Jack",15.08,7,12,200], ["05/04/2021","Lola", 11.14,11,25,314], ["05/04/2021",'Jaime', 13.45, 10,7,175],
        ["06/04/2021","Jack",16.08,5,21,245], ["06/04/2021","Lola", 13.06,13,17,330], ["06/04/2021",'Jaime', 14.35, 13,13,225],
        ["07/04/2021","Jack",14.18,9,7,227], ["07/04/2021","Lola", 11.54,14,18,347], ["07/04/2021",'Jaime', 13.07, 9,21,242],
        ["08/04/2021","Jack",13.52,11,16,260], ["08/04/2021","Lola", 10.34,15,22,354], ["08/04/2021",'Jaime', 12.45, 15,19,266]]
df_enc = pd.DataFrame(lst, columns = ['Fecha','Encuestador','Duracion_media','Encuestas_realizadas', 'Encuestas aplazadas', 'Telefonos usados'])

#df con las medias, sumas, etc
dff_enc=df_enc.groupby('Encuestador', as_index=False)[['Encuestas_realizadas','Duracion_media']].mean()
print(dff_enc[:3])



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('table', external_stylesheets=external_stylesheets)

#---------------------------------------------------------------
app.layout = html.Div([
    html.H4('Encuestadores por día'),
    #Para tabla
    html.Div([
        dash_table.DataTable(
            id='datatable_id',
            data=dff_enc.to_dict('records'),
            columns=[
                {"name": i, "id": i, "deletable": False, "selectable": False} for i in dff_enc.columns
            ],
            editable=False,
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            row_selectable="multi",
            row_deletable=False,
            selected_rows=[],

            #Elegir:
            #A - Para ver, x ej, sólo 6 filas en la tabla, numerando para pasar de página con >
            #page_action="native",
            #page_current= 0,
            #page_size= 6,

            #B - Para ver más filas con scrolldown
            page_action='none',
            style_cell={
            'whiteSpace': 'normal'
            },
            fixed_rows={ 'headers': True, 'data': 0 },
            virtualization=False,


            style_cell_conditional=[
                {'if': {'column_id': 'Encuestador'},
                 'width': '40%', 'textAlign': 'left'},
                {'if': {'column_id': 'Encuestas_realizadas'},
                 'width': '30%', 'textAlign': 'left'},
                {'if': {'column_id': 'Duracion_media'},
                 'width': '30%', 'textAlign': 'left'},
            ],
        ),
    ],className='row'),

    #Para los 2 dropdowns
    html.Div([
        html.Div([
            html.H4('Evolución de la selección'),
            dcc.Dropdown(id='linedropdown',
                options=[
                         {'label': 'Encuestas realizadas', 'value': 'Encuestas_realizadas'},
                         {'label': 'Duracion media', 'value': 'Duracion_media'}
                ],
                value='Encuestas_realizadas', #Valor por defecto
                multi=False, #Con False sólo podemos escoger un valor al mismo tiempo
                clearable=False #Con False elegirá entre las 2 labels del dropdown
            ),
        ],className='six columns'),

        html.Div([
        html.H4('Medias por encuestador'),
        dcc.Dropdown(id='piedropdown',
            options=[
                     {'label': 'Media de encuestas realizadas', 'value': 'Encuestas_realizadas'},
                     {'label': 'Duracion media', 'value': 'Duracion_media'}
            ],
            value='Encuestas_realizadas',
            multi=False,
            clearable=False
        ),
        ],className='six columns'),

    ],className='row'),

    #Para gráficos
    html.Div([
        html.Div([
            dcc.Graph(id='linechart'), #Recordar que un segundo componente sería figure={}, abajo usado en el callback
        ],className='six columns'),

        html.Div([
            dcc.Graph(id='piechart'),
        ],className='six columns'),

    ],className='row'),
])

#------------------------------------------------------------------
@app.callback(
    [Output('piechart', 'figure'),
     Output('linechart', 'figure')],
    [Input('datatable_id', 'selected_rows'),
     Input('piedropdown', 'value'),
     Input('linedropdown', 'value')]
)
def update_data(chosen_rows,piedropval,linedropval):
    #En la tabla en principio no tenemos nada seleccionado en los tips, lo hará para todos
    if len(chosen_rows)==0:
        #Metemos los Nombres por defecto (Ej para encuestadores podemos seleccionar inicialmente)
        df_filterd = dff_enc[dff_enc['Encuestador'].isin(['Jack','Lola','Jaime'])]
    else:
        print(chosen_rows)
        df_filterd = dff_enc[dff_enc.index.isin(chosen_rows)]

    pie_chart2=px.pie(
            data_frame=df_filterd,
            names='Encuestador',
            values=piedropval,
            hole=.3,
            labels={'Encuestador':'Encuestador'}
            )
    pie_chart2.update_traces(textinfo='value+percent').update_layout(title_x=0.5)

    #extract list of chosen countries
    list_chosen=df_filterd['Encuestador'].tolist()
    #filter original df according to chosen countries
    #because original df has all the complete dates
    df_line = df_enc[df_enc['Encuestador'].isin(list_chosen)]

    line_chart = px.line(
            data_frame=df_line,
            x='Fecha',
            y=linedropval,
            color='Encuestador',
            labels={'Encuestador':'Encuestador', 'Fecha':'Fecha'},
            )
    line_chart.update_layout(uirevision='foo') #Si cambiamos la visión del gráfico (ej acercando), se mantendrá en el recuadro seleccionado cuando cambiemos, por ejemplo, 
                                                #...de encuestas a teléfonos en el dropdown

    #Retornamos los outputs creados en la función
    return (pie_chart2,line_chart)