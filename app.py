import dash
from dash import Dash, html, dcc,  Input, Output, callback, State
import numpy as np
import plotly.graph_objs as go
from os import listdir
from scipy.io import wavfile
from scipy import signal

app = Dash(__name__,use_pages=True, suppress_callback_exceptions=True)



app.layout = html.Div([
    html.Div([    
         html.Div([  
            dcc.Link(page['name']+"  ", href=page['path'] , style={"margin-right": "18px",})
            for page in dash.page_registry.values() ], className='center-bar')
        
        
    ], 
    className='bar'),
              
    dash.page_container
], className='parent-div'),
html.Div(id='page-content', className='parent-div'),

print('***********8888')
print(listdir('assets'))

# @app.callback([Output('graph2', 'figure')],
#          [Input('graph-with-slider', 'relayoutData')], # this triggers the event
#          [State('graph2', 'figure')])
# def zoom_event(relayout_data, *figures):
#     outputs = []
#     for fig in figures:
#         try:
#             fig['layout']["xaxis"]["range"] = [relayout_data['xaxis.range[0]'], relayout_data['xaxis.range[1]']]
#             fig['layout']["xaxis"]["autorange"] = False
#         except (KeyError, TypeError):
#             fig['layout']["xaxis"]["autorange"] = True

#         outputs.append(fig)

#     return outputs


if __name__ == '__main__':
    app.run(debug=True)