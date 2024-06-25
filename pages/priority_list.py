import dash
from dash import html, dcc, callback, Input, Output, dash_table
#import dash_table
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import numpy as np

dash.register_page(__name__, path='/')
def convert_to_labelled_df(df, vessel_type):
    vessel_df = df[['x',vessel_type]]
    non_zero_x =vessel_df[vessel_df[vessel_type]!=0]['x']
    vessel = []
    for i in non_zero_x.index:
       # print(vessel_df.loc[i,vessel_type])
        vessel.append(vessel_df.loc[i, vessel_type])

    vessel_df = non_zero_x.to_frame()
    vessel_df[vessel_type] = vessel
    #add column named type with value vessel_type
    vessel_df['type'] = vessel_type
    return vessel_df

def read_prediction():
    df = pd.read_csv('assets/predictions/99.wav/prediction.csv')
    
    vessel_type_list = ['tanker', 'tug', 'passengership', 'cargo']
    # crate an array of data frame
    df_list = [convert_to_labelled_df(df, vessel_type) for vessel_type in vessel_type_list]
   
    
    # for df in df_list:
    #     print(df)

    # create data frame labelled_df with columns file, start_time, end, type
    labelled_df = pd.DataFrame(columns=['Filename', 'From', 'To', 'Tags'])
    #TODO loop through the files in the directory at the beginning
    file = 'assets/99.wav'
    link = []
    # loop through each data frame in df_list
    for df in df_list:
        #labelled_df.loc[len(labelled_df.index)] = ['99.wav', df['x'].iloc[0], df['x'].iloc[df.shape[0]-1], df['type'].iloc[0]]
        labelled_df.loc[len(labelled_df.index)] = ['assets/99.wav', df['x'].iloc[0], df['x'].iloc[df.shape[0]-1], df['type'].iloc[0]]       
        link.append('[Click](dashboard2?'+file+'&start='+str(df['x'].iloc[0])+'&end='+str(df['x'].iloc[df.shape[0]-1])+')')
    #add a column named link with value [Click](dashboard?audio/99.wav)
    #labelled_df['link'] = link
    labelled_df['Link(s)'] = link
    return labelled_df

def generarte_scatter():
    print('in generate scatter')
    #d = pd.read_csv('scatter_test.csv')
    d = pd.read_csv('assets/umap_train.csv')
    d = d[['X','Y','label','duration']]
    d = pd.pivot_table(
    d, index=["X","duration"], columns="label", values="Y").reset_index()   
    #replace all Nan value in d with 0
    d = d.fillna(0.0)
    #rename X with x
    d = d.rename(columns={'X': 'x'})
    #drop duration column
    d = d.drop(columns=['duration'])
    return d

df = read_prediction()
df_scatter = generarte_scatter()

#this method will be called during the initialization of the page
def get_figure():    
    fig = go.Figure(px.scatter(df_scatter, x='x', y=df_scatter.columns.values.tolist()[1:], title="Label Detection"), layout=layout)
    fig.update_layout(     
        dragmode="select",
        hovermode="closest",
        newselection_mode="gradual",
    )
    print('new figure created***********')
    return fig

layout = html.Div([   
    html.Div([
        html.Link(
            rel='stylesheet',
            href='/assests/css/styles.css'
        ),
       
        html.Div([
            html.H1('Navy AI Data Labelling Tool - Priority List', className='pageheader'),
            dash_table.DataTable(  
            data=df.to_dict('records'),       
            id="df",
            columns=[{'id': x, 'name': x, 'presentation': 'markdown'} if x == 'Link(s)' else {'id': x, 'name': x} for x in df.columns],
           # style_as_list_view=True,      
            style_data={                
                'backgroundColor': 'rgb(79, 79, 100)'
            },
            style_header={
                'backgroundColor': 'rgb(31, 31, 46)',
                'color': 'white',
                'fontWeight': 'bold'
            },
           style_cell={'height': '12px', 'minHeight': '12px', 'maxHeight': '12px','textAlign': 'center'},           
            ),
            html.Br(),
           dcc.Tooltip(id="graph-tooltip"),
            html.Div([
                html.Div(
                    dcc.Graph(id="scatter_plot_home", config={"displayModeBar": False},clear_on_unhover=True )          
                ),
            
            ])
            
       
    ], style={'width': '70%',
               },
        className='center'),
        
        html.Pre(id='hover-data')
       
    ], className='parent-div'),

],style={'height':'100vh'})

@callback(
  # Output('test_text', 'children'),
   Output('scatter_plot_home', 'figure'),
    Input("scatter_plot_home", "selectedData"), 
    Input("scatter_plot_home", "figure"),
)
def initialize_graph(selection, figure): 
    print('selection ',selection)
    if selection is None:
        fig = get_figure()
        
    #points outside plot is selected 
    elif len(selection.get('points')) == 0:
        fig = get_figure()
    else:
        print(len(selection.get('points')))
        trace = selection.get('points')[0].get('curveNumber')
        print(df_scatter.columns[trace+1])
        print('Updating Graph')
        fig = update_scatter_graph(figure, df_scatter.columns[trace+1])
    
    return  fig
    
def update_scatter_graph(fig,trace):
    print('in update scatter graph')
   
    print('trace ',trace)
    #loop through each element in list
    for i in range(len(fig['data'])):
        if fig['data'][i].get('legendgroup') == trace:
            #convert data frame columns into np.ndarray
            selectedpoints = np.array(df_scatter[trace])
         
            selectedcols = df_scatter[trace]
            print('FOUND..............', trace)
            fig['data'][i]['marker']['color'] = 'red'

    fig['data'] = []
    fig = go.Figure(px.scatter(df_scatter, x='x', y=df_scatter.columns.values.tolist()[1:], title="Label Detection"), layout=layout)
    fig.add_scatter(x=df_scatter['x'], y=selectedcols, mode='markers+lines',marker={'size':10}, showlegend=False, hoveron='points', name=trace)
    print(selectedpoints)
    # fig.update_traces(
    #     selectedpoints=selectedpoints,
    #     customdata=df_scatter.index,
    #     mode="markers",
    #     #marker={"color": "rgba(0, 116, 217, 0.7)", "size": 20},
    #     unselected={
    #         "marker": {"opacity": 0.3},
    #         "textfont": {"color": "rgba(0, 0, 0, 0)"},
    #     },
    # )
    fig.update_layout(
       # margin={"l": 20, "r": 0, "b": 15, "t": 5},
        dragmode="select",
       # hovermode=False,
       
        hoversubplots="single",
        newselection_mode="gradual",
    )

    return fig

# @callback(   

#    # Output('hover-data', 'children'),
 
#      Output("graph-tooltip", "show"),
#      Output('scatter_plot_home', 'figure',allow_duplicate=True),
#     Input('scatter_plot_home', 'hoverData'),
#     Input('scatter_plot_home', 'figure'),
#     prevent_initial_call=True)

# def display_hover_data(hoverData, figure):
#     print('in hover functionality ', hoverData)
#     if figure is None:
#         print('First time loading')
#     if hoverData is None:
#         return True,figure
#     #print(figure)
#     trace = hoverData.get('points')[0].get('curveNumber')
#     #print df column at trace index

#     #print(df.loc[:, trace])
#     print('After HOverrrrrrrrrrrrr ',trace)
#     print(df_scatter.columns[trace+1])
#     #print(figure)
#     fig1 = update_scatter_graph(figure, df_scatter.columns[trace+1])
    
#     return True,fig1

