import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

app = dash.Dash()

# df = pd.read_csv(
#     'https://gist.githubusercontent.com/chriddyp/'
#     'cb5392c35661370d95f300086accea51/raw/'
#     '8e0768211f6b747c0db42a9ce9a0937dafcbd8b2/'
#     'indicators.csv')
df = pd.read_csv('lab3-datasets/black-friday/BlackFriday.csv')

# BlackFriday.csv分析
# User_ID(Gender, Age, Occupation, City_Category, Marital_Status) : Product_Category_1 : Number
# 每位消费者喜欢哪种类型的商品
#x:User_ID; y:Product_Category_1

available_age = df['Age'].unique()
available_purchase = df['Purchase'].unique()

available_userID = df['User_ID'].unique()
avaliable_proCate = df['Product_Category_1'].unique()
available_occ = df['Occupation'].unique()

app.layout = html.Div([
    html.Div([

        # Input_age
        html.Div([
            dcc.Dropdown(
                id='crossfilter-xaxis-column', # age
                options=[{'label': i, 'value': i} for i in available_age],
                # value='User_ID'
                value='0-17'
            )
            # dcc.RadioItems(
            #     id='crossfilter-xaxis-type',
            #     options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
            #     value='Linear',
            #     labelStyle={'display': 'inline-block'}
            # )
        ],
        style={'width': '49%', 'display': 'inline-block'}),

        # Input_occupation
        html.Div([
            dcc.Dropdown(
                id='crossfilter-yaxis-column',
                options=[{'label': i, 'value': i} for i in available_occ],
                # value='Product_Category_1'
                value='15'

            )
        #     dcc.RadioItems(
        #         id='crossfilter-yaxis-type',
        #         options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
        #         value='Linear',
        #         labelStyle={'display': 'inline-block'}
        #     )
        ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
    }),
# Above is CheckBox


# Scatter Diagram
    html.Div([
        dcc.Graph(
            id='crossfilter-indicator-scatter'
            # hoverData={'points': [{'age': '0-17'}]}
        )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),


# lineChart
    html.Div([
        dcc.Graph(id='series'),

    ], style={'display': 'inline-block', 'width': '49%'}),


#Pie
    html.Div([
        dcc.Graph(id='pie'),

    ],style={'display': 'inline-block', 'width': '49%'})


])


# Scatter
@app.callback(
    dash.dependencies.Output('crossfilter-indicator-scatter', 'figure'),
    [dash.dependencies.Input('crossfilter-xaxis-column', 'value')])
     # dash.dependencies.Input('crossfilter-age', 'value'),
     # dash.dependencies.Input('crossfilter-xaxis-type', 'value'),
     # dash.dependencies.Input('crossfilter-yaxis-type', 'value'),
     # dash.dependencies.Input('crossfilter-occ--slider', 'value')])
def update_graph(age_value):

    dff = df[df['Age'] == age_value]
    return {
        'data': [go.Scatter(
            x=dff['Product_Category_1'],
            y=dff['Purchase'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': 'Product_Category_1'
                #'type': 'linear' if xaxis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': 'Purchase'
                #'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
            height=450,
            hovermode='closest'
        )
    }



# Pie: According to Product_Category_1, rate of F and M(Gender)
@app.callback(
    dash.dependencies.Output('pie', 'figure'),
    [dash.dependencies.Input('crossfilter-yaxis-column', 'value')])
     # dash.dependencies.Input('base-occupation','value')])

def create_gender_pie(pro_cate):
    dff_cate = df[df['Product_Category_1'] == pro_cate]
    # total = df.shape[0]
    counts = dff_cate['Gender'].value_counts(ascending=True,normalize=True).tolist()
    # print(counts)
    # print(counts[0])
    # print(counts[1])

    return {
        'data': [go.Pie(
            labels=['F','M'],
            values=[counts[0],counts[1]]
        )]
        # 'layout': {
        #     'height': 225,
        #     'margin': {'l': 20, 'b': 30, 'r': 10, 't': 10},
        #     'annotations': [{
        #         'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
        #         'xref': 'paper', 'yref': 'paper', 'showarrow': False,
        #         'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
        #         'text': title
        #     }],
            # 'yaxis': {'type': 'linear' if axis_type == 'Linear' else 'log'},
            # 'xaxis': {'showgrid': False}
#        }
    }


# Series
@app.callback(
    dash.dependencies.Output('series', 'figure'),
    [dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-column', 'value')])
     # dash.dependencies.Input('crossfilter-xaxis-type', 'value'),
     # dash.dependencies.Input('crossfilter-yaxis-type', 'value'),
     # dash.dependencies.Input('crossfilter-occ--slider', 'value')])
def series(age_value, procate_value):
                 # , yaxis_column_name,
                 # xaxis_type, yaxis_type,
                 # occ_value):
    dff = df[df['Age'] == age_value]
    dff_procate = dff[dff['Product_Category_1']==procate_value]
    return {
        'data': [go.Scatter(
            x=dff_procate['User_ID'],
            y=dff_procate['Purchase'],
            # text=dff[dff['User_ID'] == yaxis_column_name]['Product_ID'],
            # customdata=dff[dff['User_ID'] == yaxis_column_name]['Product_ID'],
            mode='lines+markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': 'User_ID'
                #'type': 'linear' if xaxis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': 'Purchase'
                #'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
            height=450,
            hovermode='closest'
        )
    }




app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

if __name__ == '__main__':
    app.run_server(port='8060')