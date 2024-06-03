import dash
from dash import html, dcc, callback, Input, Output, dash_table
#import dash_table
import pandas as pd

dash.register_page(__name__, path='/')
def convert_to_labelled_df(df, vessel_type):
    vessel_df = df[['x',vessel_type]]
    non_zero_x =vessel_df[vessel_df[vessel_type]!=0]['x']
    vessel = []
    for i in non_zero_x.index:
        print(vessel_df.loc[i,vessel_type])
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


df = read_prediction()

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
       
       
    ], style={'width': '70%',
               },
        className='center'),
    
    ], className='parent-div'),

],style={'height':'100vh'})


    
    
print(df.head())
