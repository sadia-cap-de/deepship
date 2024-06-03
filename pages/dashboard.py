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
def generarte_line_for_audio():
    df = pd.read_csv('assets/predictions/99.wav/prediction.csv')
    x1 = 3
    x2 = 10

    #extract dataframe from df where x is between x1 and x2
    df = df[df['x'].between(x1,x2)]
    print(df)
    #if all rows of a column has all 0.0 value then drop that column
    df = df.loc[:, (df != 0).any(axis=0)]
    fig = go.Figure(px.line(df, x='x', y=df.columns.values.tolist()[1:], title="Label Detection"), layout=layout)
    fig.update_layout(showlegend=True,legend_title_text='Labels')
    return fig

def audio_len_for_slider(file):
   #get duration of audio file in python
    fs, data = wavfile.read(file)
    duration = len(data)/fs
    print('Duration ', duration)
    return duration


duration = int(audio_len_for_slider('assets/99.wav'))
#fig = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[4, 1, 2])], layout=layout)
fig = generarte_line_for_audio()

def blank_fig():
    fig = go.Figure(go.Scatter(x=[], y = []))
    fig.update_layout(template = None)
    fig.update_xaxes(showgrid = False, showticklabels = False, zeroline=False)
    fig.update_yaxes(showgrid = False, showticklabels = False, zeroline=False)
    
    return fig

def spectogram(x1,x2):
    """
    convert_audio_to_spectogram -- using librosa to simply plot a spectogram
    Arguments:
    filename -- filepath to the file that you want to see the waveplot for
    
    Returns -- None
    """
    print('****8generating specogram********')
    filename = 'assets/99.wav'
    
    fig, ax = plt.subplots(figsize=(14, 5))
   
    #plt.figure(figsize=(14, 5))
    # sr == sampling rate 
    x, sr = librosa.load(filename, sr=32000)
    x = x[x1*32000:x2*32000]
    
    # stft is short time fourier transform
    X = librosa.stft(x)
    
    # convert the slices to amplitude
    Xdb = librosa.amplitude_to_db(abs(X))
    
    # ... and plot, magic!
   
    
    librosa.display.specshow(Xdb, sr = sr, x_axis = 'time', y_axis = 'hz', ax = ax)
    #plt.show()
   # print(type(img))
    
   # ax.imshow(Xdb, aspect='auto', origin='lower')
    #ax.set(title='Now with labeled axes!')
    #fig.colorbar(img, ax=ax, format="%+2.f dB")
    

    buf = io.BytesIO() # in-memory files
    # #plt.scatter(x, y)
    plt.savefig(buf, format = "png")
    plt.close()
    data = base64.b64encode(buf.getbuffer()).decode("utf8") # encode to html elements
    buf.close()
    return "data:image/png;base64,{}".format(data)
    #return fig
    #librosa.display.specshow(Xdb)
    #plt.ylabel('Frequency [Hz]')
    #plt.xlabel('Time [sec]')
layout = html.Div([
         html.Link(
            rel='stylesheet',
            href='/assests/css/styles.css'
        ),
        html.Div([
        html.H1('Navy AI Data Labelling Tool - Dashboard', className='pageheader'),
        
        html.Div(dcc.Graph(id='graph-with-slider', 
            figure=fig,
           )),
       
        html.Br(),
        html.Audio(src="http://localhost:8050/assets/99.wav",  preload="auto",controls=True, style={"width":"100%"}) ,
        
    dcc.Store(id='file_name', storage_type='memory'),
    html.Div( html.Br()),  
       
    html.Div(dcc.RangeSlider(0, duration, 5, id='my-range-slider', value=[1,3])),               
    
    dcc.Location(id='url', refresh=False),
    html.Div(id='content'),   
    
    html.Img(src=spectogram(0,duration),id='spectogram-graph', width=1070, height=471),
    #html.Div(dcc.Graph(id='spectogram-graph', figure = blank_fig())),
    ], className='center')
    ], className='parent-div')
 
#layout = layout()

########## page loading url ############
@callback(Output('file_name', 'data'), Input('url', 'href'))
def display_page(url):
    print('******** url ',url)
    param = url.split('?')
    #check if param has two element 
    if len(param) != 2:
        return None
    #TODO check if url exist
    file_name = param[1]
    print('????? ',param)
    
    return file_name
  


    

# def spectogram(file):
#     fs, Audiodata = wavfile.read(file)  
   
#     N = 512 #Number of point in the fft
#     w = signal.windows.blackman(N)
#     freqs, bins, Pxx = signal.spectrogram(Audiodata, fs,window = w,nfft=N)
#     np.seterr(divide = 'ignore')
#     # Plot with plotly
#     trace = [go.Heatmap(
#         x= bins,
#         y= freqs,
#         z= 10*np.log10(Pxx),
#         colorscale='Magma'
#         )]
#     layout = go.Layout(
#         title = 'Spectrogram with plotly',
#         yaxis = dict(title = 'Frequency'), # x-axis label
#         xaxis = dict(title = 'Time'), # y-axis label
#         )
#     fig = go.Figure(data=trace, layout=layout)
#     return fig

def load_audio(file):
    audio_file = f'assets/{file}.wav'
    return audio_file

  

# @callback(Output('my-range-slider', 'value'),
#               [Input('graph-with-slider', 'relayoutData')],
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
#         return value
    
    
    #value = [relayoutData[xaxis.range[0]],xaxis.range[1]]

@callback(
    Output('graph-with-slider', 'figure',allow_duplicate=True),
    Input('my-range-slider', 'value'),
    State('graph-with-slider', 'figure'),
    
    prevent_initial_call=True
    )

def update_output(value,figure):
   # print(value)
    if figure is None:
        return None
    #print(figure)
    print(type(value))
    #figure['layout']['xaxis'] = {'range': (1, 10)}
    figure['layout']['xaxis'] = {'range': value, 'autorange': False}
    return figure

@callback(
    Output('spectogram-graph', 'src',allow_duplicate=True),    
    Input('my-range-slider', 'value'),
    State('spectogram-graph', 'src'),
    
    prevent_initial_call=True)

def update_output(value,figure):
   # print(value)
    if figure is None:
        return None
    #print(figure)
    print(type(value))
    img = spectogram(value[0], value[1])

    #figure['layout']['xaxis'] = {'range': (1, 10)}
    #figure['layout']['xaxis'] = {'range': value, 'autorange': False}
    return img


# @callback(
#     Output('spectogram-graph', 'figure',allow_duplicate=True),
    
#     Input('submit-button', 'n_clicks'),
#     State('file_name', 'data'),
#     prevent_initial_call=True
# )
# def generate_specto(n_clicks, data):
#     if n_clicks is None:
#         return None
#     print('generating specto for file ', data)
   
#     figure = spectogram(data)
#     import plotly
#     return plotly.tools.mpl_to_plotly(figure)
#, {'display': 'block'}