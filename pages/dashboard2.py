import dash
from dash import html, dcc, callback, Input, Output, State
import numpy as np
import plotly.graph_objs as go
import pandas as pd
import matplotlib.pyplot as plt 

import io
import base64

from os import listdir
from scipy.io import wavfile
from scipy import signal
import plotly.express as px
import librosa

#setting default value for audio fileaudio_file = 'assets/99.wav'

dash.register_page(__name__)
layout = go.Layout(
    paper_bgcolor='rgba(0,0,0,0)'
  
)
global file_name_dashboard2
def generarte_line_for_audio(x1,x2):
    df = pd.read_csv('assets/predictions/99.wav/prediction.csv')
    # x1 = 3
    # x2 = 10

    #extract dataframe from df where x is between x1 and x2
    df = df[df['x'].between(x1,x2)]
    print(df)
    #if all rows of a column has all 0.0 value then drop that column
    df = df.loc[:, (df != 0).any(axis=0)]
    #rename column from x to time
    df = df.rename(columns={'x': 'time'})
    fig = go.Figure(px.line(df, x='time', y=df.columns.values.tolist()[1:], title="Vessel Classification"), layout=layout)
    fig.update_layout(showlegend=True,legend_title_text='Vessel Class')
    return fig

def audio_len_for_slider(file):
   #get duration of audio file in python
    fs, data = wavfile.read(file)
    duration = len(data)/fs
    print('Duration ', duration)
    return duration




def spectogram(file):
    file = 'assets/99.wav'
    fs, Audiodata = wavfile.read(file)  
   
    N = 512 #Number of point in the fft
    w = signal.windows.blackman(N)
    freqs, bins, Pxx = signal.spectrogram(Audiodata, fs,window = w,nfft=N)
    np.seterr(divide = 'ignore')
    # Plot with plotly
    trace = [go.Heatmap(
        x= bins,
        y= freqs,
        z= 10*np.log10(Pxx),
        colorscale='Magma'
        )]
    layout = go.Layout(
        title = 'Spectrogram with plotly',
        yaxis = dict(title = 'Frequency'), # x-axis label
        xaxis = dict(title = 'Time'), # y-axis label
        )
    fig = go.Figure(data=trace, layout=layout)
    return fig

#this is hard coded value passed for slider
duration = int(audio_len_for_slider('assets/99.wav'))



layout = html.Div([
         html.Link(
            rel='stylesheet',
            href='/assests/css/styles.css'
        ),
       # dcc.Store(id='file_name_dashboard2', storage_type='memory', data=file_name_dashboard2),
        html.Div([
        html.H1('Navy AI Data Labelling Tool - Dashboard', className='pageheader'),
        
        html.Div(dcc.Graph(id='graph-with-slider'
           # figure=fig,
           )),
       
        html.Br(),
        html.Audio(src="http://localhost:8050/assets/99.wav",  preload="auto",controls=True, style={
            "width": "90%"
        }) ,
        
       
   
      
    html.Div(dcc.RangeSlider(0, duration,  id='range-slider', value=[1,3]),style={"width": "100%"}),       

    html.Div(id='slider_selection_text',children=[], style={"font-weight":"bold", "font-family":"Arial, Helvetica, sans-serif;"}),
    html.Div( html.Br(),),

    dcc.Location(id='url', refresh=False),
    html.Div(id='content'),   
    
    #html.Img(src=spectogram(),id='spectogram-graph', width=1070, height=471),
    html.Div(dcc.Graph(id='spectogram-graph-plotly')),
    ], className='center')
    ], className='parent-div')
 
#layout = layout()

########## page loading url ############
@callback(
        #Output('file_name_dashboard2', 'data'),
          Output('spectogram-graph-plotly', 'figure',allow_duplicate=True),
          #State('spectogram-graph-plotly', 'figure'),      
        Input('url', 'href'),
        prevent_initial_call='initial_duplicate')
def display_page(url):
    print('******** url ',url)
    param = url.split('?')
    #check if param has two element 
    if len(param) != 2:
        return None
    #TODO check if url exist
    file_name = param[1]
    print('????? ',param)
    figure = spectogram(file_name)     
    
    return  figure 

@callback(
        #Output('file_name_dashboard2', 'data'),
          Output('graph-with-slider', 'figure',allow_duplicate=True),
          #State('spectogram-graph-plotly', 'figure'),      
        Input('url', 'href'),
        prevent_initial_call='initial_duplicate')
def display_page(url):
    print('******** url ',url)
    param = url.split('?')[1].split('&')
    #check if param has two element 
    if len(param) != 3:
        return None
    #TODO check if url exist
    # file_name = param[1]
    # print('????? ',param)
    # figure = spectogram(file_name)     
    start = int(param[1].split('=')[1])
    end = int(param[2].split('=')[1])
    figure = generarte_line_for_audio(start,end)
    return  figure 
  


    


def load_audio(file):
    audio_file = f'assets/{file}.wav'
    return audio_file

  

# @callback(Output('range-slider', 'value'),
#          # Output(component_id='slider_selection_text', component_property='children'),
#               [Input('spectogram-graph-plotly', 'relayoutData')],
#               #State('graph-with-slider', 'figure'),
#               prevent_initial_call=True
#               )
# def display_relayout_data(relayout_data):
#     print('in relay layout')
#     # for key, value in relayout_data.items():
#     #     print(key, value)
#     #print(relayout_data['xaxis.range[0]'])  
#     if relayout_data is None:
#         return None
#     else:
#         if "xaxis.range[0]" not in relayout_data and "xaxis.range[1]" not in relayout_data:
#             return None
#         value = [relayout_data["xaxis.range[0]"],relayout_data["xaxis.range[1]"]]
#         print('relay*** ',value)
#         select_text = "Selection : "+str(value[0])+" - "+str(value[1])
#         return value
    
    
    #value = [relayoutData[xaxis.range[0]],xaxis.range[1]]

# @callback(
#     Output('spectogram-graph-plotly', 'figure'),
#     Output('slider_selection_text', 'children',allow_duplicate=True),
#     Input('range-slider', 'value'),
#     State('spectogram-graph-plotly', 'figure'),
#     prevent_initial_call=True
#     )

# def update_output(value,figure):
#    # print(value)
#     if figure is None:
#         return None,""
#     #print(figure)
#     print(value)
#     #figure['layout']['xaxis'] = {'range': (1, 10)}
#     figure['layout']['xaxis'] = {'range': value, 'autorange': False}
    
#     if value is None:
#         select_text = ""
#     else:
#         select_text = "Selection : "+str(value[0])+" - "+str(value[1])
#     return figure, select_text

@callback(
    Output('spectogram-graph-plotly', 'figure'),
    Output('slider_selection_text', 'children'),
    Input('range-slider', 'value'),
    State('spectogram-graph-plotly', 'figure'),
    prevent_initial_call=True)

def update_output(value,figure):
   # print(value)
    if figure is None:
        return None,""
    #print(figure)
    print(value)
    #figure['layout']['xaxis'] = {'range': (1, 10)}
    figure['layout']['xaxis'] = {'range': value, 'autorange': False}
    if value is None:
        select_text = ""
    else:
        select_text = "Selection : "+str(value[0])+" - "+str(value[1])
    return figure,select_text



