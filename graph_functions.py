import urllib2
import csv
import codecs
import data as d
import plotly.plotly as py
from plotly.graph_objs import *
import numpy as np
from scipy import stats

'''Graphing functions'''

def scatterPlot(xList, yList, xLabel, yLabel, title, names):
    data = Data([Scatter(
            x=xList,
            y=yList,
            mode='markers',
            text=names,
        )])

    layout = Layout(
        title=title,
        xaxis=XAxis(
            title= xLabel,
            showgrid=False,
            zeroline=False
        ),
        yaxis=YAxis(
            title= yLabel,
            showline=False
        )
    )
    fig = Figure(data=data, layout=layout)
    return fig

def barGraph(labels, frequencies, xLabel, yLabel, title):
    data = Data([Bar(
            x=labels,
            y=frequencies,
        )])

    layout = Layout(
        title= title,
        xaxis=XAxis(
            title=xLabel,
            showgrid=False,
            zeroline=False
        ),
        yaxis=YAxis(
            title= yLabel,
            showline=False
        )
    )
    fig = Figure(data=data, layout=layout)
    plot_url = py.plot(fig, filename=title)

def histogramT(x1, x2, x3, n1='1', n2='2', n3='3'):
    low = Histogram(
        x=x1,
        opacity=0.50,
        name = n1
    )
    mid = Histogram(
        x=x2,
        opacity=0.50,
        name = n2
    )

    high = Histogram(
        x=x3,
        opacity=0.50,
        name = n3
    )

    data = Data([low, mid, high])
    
    layout = Layout(
        barmode='overlay'
    )
    fig = Figure(data=data, layout=layout)
    return fig
    
def histogramTwo(x1, x2, n1, n2):
    low = Histogram(
        x=x1,
        opacity=0.50,
        name = n1
    )
    high = Histogram(
        x=x2,
        opacity=0.50,
        name = n2
    )

    data = Data([low, high])
    
    layout = Layout(
        barmode='overlay'
    )
    fig = Figure(data=data, layout=layout)
    return fig

def histogram(x):
    data = Data([
        Histogram(
            x=x
        )
    ])
    return data
