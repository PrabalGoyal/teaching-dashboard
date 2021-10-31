import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
import plotly
import plotly.graph_objs as go
import dash_bootstrap_components as dbc

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, routes_pathname_prefix='/student/',external_stylesheets=[dbc.themes.BOOTSTRAP],meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])
# routes_pathname_prefix='/teacher/'
df = pd.read_excel('Book2.xlsx')


# replacable values as & when request given
District = 1
Zone_no = 1
School_no = 1

# new df containing data of particular school only
ndf = df[(df['Distt']==District) & (df['Zone']==Zone_no) & (df['School']==School_no)]
# newdf = df[(df['Distt'] == District) & (df['Zone'] == Zone_no)]
app.config['suppress_callback_exceptions'] = True

# **--------------------------------------app layout-----------------------------------**

app.layout = html.Div(
    children=[
    dcc.Location(id='url', refresh=False),
    html.Div([
    html.H2('Student Dashboard'),
    html.H2(id='s'),
    #Graph A: all subjects
    html.Div([
            html.Div(dcc.Graph(id='all-subs-graph',config={"displaylogo": False,}),style={}),
        ], style={'text-align':'center'}),
    
    html.Div([
    #filters
        html.Div([
            html.Div([
            html.Div([
                html.Label(["Choose Subject"],style={'float':'left'}),
                html.Div([
                dcc.Dropdown(id='dd_sub',clearable=False,style={'text-align':'left'},)],style={'float':'right','width':'90px'}),
            ],style={'margin-bottom':'10px'})
            ] ,style={}),
        ],style={}),

     # avgs
        # html.Div([
        #     html.Div([
        #     html.Div([
        #             html.Div([
        #             html.Div(html.P(id='pass'),className="row justify-content-sm-center",style={'font-size':'250%',"text-align":"center","justify-content":"center","align-items":"center"}),
        #             html.Div(html.P('Pass Percentage'),className="row justify-content-sm-center",style={"text-align":"center","justify-content":"center","align-items":"center"}),
        #             ],className="col-sm-4 ",style={"text-align":"center"}),

        #             html.Div([
        #             html.Div(html.P(id='pass90'),className="row justify-content-sm-center",style={'font-size':'250%',"text-align":"center","justify-content":"center","align-items":"center"}),
        #             html.Div(html.P('Students above 90%'),className="row justify-content-sm-center",style={"text-align":"center","justify-content":"center","align-items":"center"}),
        #             ],className="col-sm-4 ",style={"text-align":"center"}),

        #             html.Div([
        #             html.Div(html.P(id='pass75'),className="row justify-content-sm-center",style={'font-size':'250%',"text-align":"center","justify-content":"center","align-items":"center"}),
        #             html.Div(html.P('Students above 75%'),className="row justify-content-sm-center",style={"text-align":"center","justify-content":"center","align-items":"center"}),
        #             ],className="col-sm-4 ",style={"text-align":"center"}),

        #             html.Div([
        #             html.Div(html.P(id='fail'),className="row justify-content-sm-center",style={'font-size':'250%',"text-align":"center","justify-content":"center","align-items":"center"}),
        #             html.Div(html.P('Students Failed'),className="row justify-content-sm-center",style={"text-align":"center","justify-content":"center","align-items":"center"}),
        #             ],className="col-sm-4 ",style={"text-align":"center"}),

        #             html.Div([
        #             html.Div(html.P(id='fail1'),className="row justify-content-sm-center",style={'font-size':'250%',"text-align":"center","justify-content":"center","align-items":"center"}),
        #             html.Div(html.P('Students failed in 1 Subject'),className="row justify-content-sm-center",style={"text-align":"center","justify-content":"center","align-items":"center"}),
        #             ],className="col-sm-4 ",style={"text-align":"center"}),

        #             html.Div([
        #             html.Div(html.P(id='fail2'),className="row justify-content-sm-center",style={'font-size':'250%',"text-align":"center","justify-content":"center","align-items":"center"}),
        #             html.Div(html.P('Students failed in 1 Subject'),className="row justify-content-sm-center",style={"text-align":"center","justify-content":"center","align-items":"center"}),
        #             ],className="col-sm-4 ",style={"text-align":"center"}),

        #     ], className="row justify-content-xs-center",style={}),
        #     ],className="container"),
        #  ],className="col-lg-5",style={}),

    ],className="row", style={'margin-bottom':'10px','margin-top':'20px'}),
    ],className="container-fluid",style={'margin-bottom':'10px'}),

    # graphs
        html.Div([
        html.Div([
            # html.Div(className="col-lg-1",style={}),
            html.Div(dcc.Graph(id='topic-imp-graph',config={"displaylogo": False,}), className="col-lg-6",style={}),
            html.Div(dcc.Graph(id='topic-wise-score-graph',config={"displaylogo": False,}),className="col-lg-6",style={}),
        ], className="row",style={'text-align':'center'}), ],className="container-fluid")

    ],style={'background-color': '#FFFFFF','width':'100%','text-align':'center'}
    )

# **--------------------------------------callbacks-----------------------------------**

@app.callback(
    Output('s', 'children'),
    [Input('url', 'pathname')]
)
def update_s(sid):
    sdf = ndf[ndf['Student'] == int(sid[9:])]
    return sdf['Subject Category'].iloc[0]

#Graph A: all subjects
@app.callback(
    Output('all-subs-graph', 'figure'),
    [Input('url', 'pathname')]
)
def update_graph_A(sid):
    sdf = ndf[ndf['Student'] == int(sid[9:])]
    # sdf = ndf[ndf['Student'] == 1]
    subs = sdf['Subject Category'].unique()
    student_score = []
    for i in subs:
        student_score.append(int(sdf[sdf['Subject Category']==i]['Total']))
    class_avg = []
    for i in range(len(subs)):
        class_avg.append(round(ndf[(ndf['Class']==sdf['Class'].iloc[0]) & (ndf['Section']==sdf['Section'].iloc[0]) & (ndf['Subject Category']==subs[i])]["Total"].mean()))
    distt_avg = [] 
    for i in range(len(subs)):
        distt_avg.append(round(ndf[(ndf['Distt']==sdf['Distt'].iloc[0]) & (ndf['Zone']==sdf['Zone'].iloc[0]) & (ndf['Class']==sdf['Class'].iloc[0]) & (ndf['Subject Category']==subs[i])]["Total"].mean()))

    #score 2D list
    score = []
    score.append(student_score)
    score.append(class_avg)
    score.append(distt_avg)    
        
    #graph
    figA = go.Figure()
    colour = ['#0DDDA4','#E8B306','#B461F5']

    # #try making colour a 2d array
    # colour = ['#AABBDE'] * (len(score[0])*len(score))
    # for i in range(len(score[0])):
    #     if score[0][i] < score[1][i] and score[0][i] < score[2][i]:
    #         colour[i*3] = '#ce0c0c'
    #     elif score[0][i] < score[1][i] or score[0][i] < score[2][i]:
    #         colour[i*3] = '#feb204'
    #     else:
    #         colour[i*3] = '#109e0e'

    col_names = ['Score','Class','Distt']
    for i in range(len(score)):
        figA.add_trace(go.Bar(
                x=subs,
                y=score[i],
                name=col_names[i],
                text=score[i],
                textposition='outside',
                texttemplate='%{text}%',            
                marker_color = colour[i],
                width=0.2
            ))

    figA.update_layout(barmode='group',
                        title='<b>Student Performance</b>', title_x=0.5, title_y=0.9,
                        legend=dict(y=-0.1,x=0.15, font_size=10),legend_orientation="h",
                        xaxis=dict(showline=False,showgrid=False,zeroline=True,),  
                        plot_bgcolor='white',                
                        yaxis=dict(showgrid=True,gridcolor='#E5ECF6',showline=False,zeroline=True,range=[0,100],nticks=20),   
                        )
    return figA


# subject dropdown
@app.callback(
    [Output('dd_sub', 'options'),
     Output('dd_sub', 'value')],
    [Input('url', 'pathname')]
)
def update_dd_class(sid):
    sdf = ndf[ndf['Student'] == int(sid[9:])]
    options = [{'label': i, 'value': i} for i in sdf['Subject Category']]
    value = sdf['Subject Category'].iloc[0]
    return options, value

# stickers


# Graph B: topic importance
@app.callback(
    Output('topic-imp-graph', 'figure'),
    [Input('url', 'pathname'),
    Input('dd_sub', 'value')]
)
def update_graph_B(sid, selected_sub):
    # sdf = ndf[ndf['Student'] == int(sid[9:])]
    subdf = df[df['Subject Category']==selected_sub]
    labels = [idx for idx in subdf.columns if idx.startswith('Topic')]
    values=[]
    for i in range(len(labels)):
        values.append(subdf[labels[i]].iloc[0])
    figB = go.Figure(data=[go.Pie(labels=labels,
                                values=values)])
    figB.update_traces(title='<b>Topic Importance</b>',hoverinfo='label', textinfo='percent', textfont_size=20,
                    marker=dict(line=dict(color='white', width=1)))
    return figB

#Graph C: Topic wise score
@app.callback(
    Output('topic-wise-score-graph', 'figure'),
    [Input('url', 'pathname'),
    Input('dd_sub', 'value')]
)
def update_graph_C(sid, selected_sub):
    #df of only this student
    sdf = ndf[ndf['Student'] == int(sid[9:])]
    subdf = sdf[sdf['Subject Category']==selected_sub]

    topics = [idx for idx in subdf.columns if idx.startswith('Topic')]
    score = []
    for i in range(len(topics)):
        score.append(subdf[topics[i]].iloc[0])

    figC = go.Figure()
    colour = ['#0DDDA4','#E8B306','#B461F5', '#bcf542','#0ee3e3']
    figC.add_trace(go.Bar(
            x=topics,
            y=score,
            text=score,
            textposition='outside',
            texttemplate='%{text}%', 
            marker_color = colour,
            width=0.2
        ))
    figC.update_layout( title='<b>Performance in Subject</b>' + str(selected_sub), title_x=0.5, title_y=0.9,
                        legend=dict(y=-0.1,x=0.15, font_size=10),legend_orientation="h",
                        xaxis=dict(showline=False,showgrid=False,zeroline=True,),  
                        plot_bgcolor='white',                
                        yaxis=dict(showgrid=True,gridcolor='#E5ECF6',showline=False,zeroline=True,nticks=20),   
                        )
    return figC



if __name__ == '__main__':
    app.run_server(debug=True)
