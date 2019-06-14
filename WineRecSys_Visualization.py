# !pip install dash==0.39.0
# this version of dash has multioutput

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
import flask
import glob
import os
import pandas as pd
import numpy as np

# READ DATA
links = pd.read_csv('/home/dsc/Repos/TFM/Data/Links.csv', usecols=['Wine_Id', 'product_link', 'image_link'])
wines = pd.read_csv('/home/dsc/Repos/TFM/Data/Wines.csv',
                    usecols=['Wine_Id','Name','Type','DO','Grape','Ageing','Sight','Smell','Taste','Pairing'])

df = pd.merge(wines[['Wine_Id', 'Name']], links, how='inner', left_on='Wine_Id', right_on='Wine_Id')

coocc = pd.read_csv('/home/dsc/Repos/TFM/Data/Coocc.csv')

# DIC
dic_name = df.set_index('Wine_Id')['Name'].to_dict()
dic_image = df.set_index('Wine_Id')['image_link'].to_dict()

# FUNCTIONS
def co_occurrance_similarity(Wine_Id, coocurrance, ntop=10):
    coocurrance = coocurrance.sort_values(by = str(Wine_Id))
    similarwines = coocurrance[Wine_Id:][::-1]
    df = pd.DataFrame()
    df['Wine_Id'] = similarwines.iloc[0:ntop][str(Wine_Id)].index
    df['Value'] = similarwines.iloc[0:ntop][str(Wine_Id)].values
    df.sort_values(by='Value', ascending=False, inplace=True)
    return np.array(df)

def co_occurrance_recommendation(items_id, cooccurrance, ntop=5):
    list_sim_items = np.vstack([co_occurrance_similarity(id_, cooccurrance, ntop*10) for id_ in items_id])
    largest_freq = pd.DataFrame(list_sim_items, columns=['id', 'freq']).groupby('id').agg(max).reset_index()
    # remove wines itself
    largest_freq = largest_freq[~largest_freq['id'].isin(items_id)]     
    sorted_list = largest_freq.sort_values(by='freq', ascending=False)
    out = sorted_list.values[:ntop, 0]
    return out

# 
app = dash.Dash()

app.layout = html.Div(
    
    children = [
        html.H1('Wine System Recommender', style={'color': 'black'}),
        html.Div([
                html.Div([
                    html.H3('Please, select the wines you like:', style={'color': 'black'}),
                    dcc.Dropdown(
                        id='image-dropdown',
                        options=[{'label': dic_name[i], 'value': i} for i in range(0,366)],
                        multi = True,
                        value=[5,150]
                        ),
                    html.Br(),
                    html.Img(id='img1'),
                    html.Img(id='img2'),
                    html.Img(id='img3'),
                    html.Img(id='img4'),
                    html.Img(id='img5'),
                    html.Img(id='img6'),
                    html.Img(id='img7'),
                    html.Img(id='img8'),
                    html.Img(id='img9'),
                    html.Img(id='img10')  
                ], className="six columns"),

                html.Div([
                    html.H3('... well, so we recommend this for you:', style={'color': 'black'}),
                    html.Br(),html.Br(),html.Br(),html.Br(),
                    html.Div([
                        html.Img(id='img_r1'),  
                        html.Img(id='img_r2'),
                        html.Img(id='img_r3'),
                        html.Img(id='img_r4'),
                        html.Img(id='img_r5')
                    ])    
                ], className="six columns")
            ],
            className="row"),
        html.Br(),
        html.H3('See more details...', style={'color': 'black'}),
        html.H4('The wines you like:'),
        dash_table.DataTable(id='mytable_like',
                        style_data={'whiteSpace': 'normal'},
                        css=[{
                            'selector': '.dash-cell div.dash-cell-value',
                            'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
                        }],
                        columns=[
                             {'name': 'NAME', 'id': 'Name'},
                             {'name': 'TYPE', 'id': 'Type'},
                             {'name': 'DO', 'id': 'DO'},
                             {'name': 'GRAPE', 'id': 'Grape'},
                             {'name': 'AGEING', 'id': 'Ageing'},
                             {'name': 'SIGHT', 'id': 'Sight'},
                             {'name': 'SMELL', 'id': 'Smell'},
                             {'name': 'TASTE', 'id': 'Taste'},
                             {'name': 'PAIRING', 'id': 'Pairing'}
                         ]),
        html.H4('The wines we recommend for you:'),
        dash_table.DataTable(id='mytable_reco',
                        style_data={'whiteSpace': 'normal'},
                        css=[{
                            'selector': '.dash-cell div.dash-cell-value',
                            'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
                        }],
                        columns=[
                             {'name': 'NAME', 'id': 'Name'},
                             {'name': 'TYPE', 'id': 'Type'},
                             {'name': 'DO', 'id': 'DO'},
                             {'name': 'GRAPE', 'id': 'Grape'},
                             {'name': 'AGEING', 'id': 'Ageing'},
                             {'name': 'SIGHT', 'id': 'Sight'},
                             {'name': 'SMELL', 'id': 'Smell'},
                             {'name': 'TASTE', 'id': 'Taste'},
                             {'name': 'PAIRING', 'id': 'Pairing'}
                         ])
    ])

    
app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

@app.callback(
    [    
    dash.dependencies.Output('img1', 'src'),
    dash.dependencies.Output('img2', 'src'),
    dash.dependencies.Output('img3', 'src'),
    dash.dependencies.Output('img4', 'src'),
    dash.dependencies.Output('img5', 'src'),
    dash.dependencies.Output('img6', 'src'),
    dash.dependencies.Output('img7', 'src'),
    dash.dependencies.Output('img8', 'src'),
    dash.dependencies.Output('img9', 'src'),
    dash.dependencies.Output('img10', 'src'),
    dash.dependencies.Output('img_r1', 'src'),
    dash.dependencies.Output('img_r2', 'src'),
    dash.dependencies.Output('img_r3', 'src'),
    dash.dependencies.Output('img_r4', 'src'),
    dash.dependencies.Output('img_r5', 'src'),
    Output('mytable_like', 'data'),
    Output('mytable_reco', 'data'),
    ],
    [dash.dependencies.Input('image-dropdown', 'value')])

def update_image_src(value):
    # value: id wines like
    # a: image like
    a = []
    for i in range(0,len(value)):
        a.append(dic_image[value[i]])
    for j in range(len(value),10):
        a.append('')
    # b: id wines recommended
    b = co_occurrance_recommendation(value, coocc, 5)
    len(b)
    # c: image recommended
    c = []
    for k in range(0,5):
        c.append(dic_image[b[k]])
    wines_like = wines[wines['Wine_Id'].isin(value)].to_dict('rows')
    wines_reco = wines[wines['Wine_Id'].isin(b)].to_dict('rows')
    return a[0],a[1],a[2],a[3],a[4],a[5],a[6],a[7],a[8],a[9],c[0],c[1],c[2],c[3],c[4],wines_like,wines_reco

if __name__ == '__main__':
    app.run_server(debug=True)