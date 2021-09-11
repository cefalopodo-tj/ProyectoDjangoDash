from django.shortcuts import render
from plotly.offline import plot
import plotly.graph_objs as go

# Create your views here.

def home(requests):
    #44:57 Vista para renderizar
    def scatter():
        #Eje abcisas
        x1=[1,2,3,4]
        #Eje ordenadas
        y1=[30,35,25,45]
        #Configuramos el rastro
        trace=go.Scatter(
            x=x1,
            y=y1
        )
        #Configuramos el layout
        layout=dict(
            title='Gráfico de dispersión',
            xaxis=dict(range=[min(x1), max(x1)]),
            yaxis= dict(range= [min(y1), max(y1)])
        )
        #Creamos el dibujo
        fig = go.Figure(data=[trace], layout=layout)
        #Creamos el plot
        plot_div= plot(fig, output_type ='div', include_plotlyjs=False)
        return plot_div
    #48:25 Creamos el contexto
    context={
        #Metemos la función de arriba
        'plot': scatter()
    }

    # 48:45 añadimos el contexto al renderizado - Vamos a welcome.html
    return render(requests, 'home/welcome.html', context)




