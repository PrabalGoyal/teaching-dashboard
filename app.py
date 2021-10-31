import dash
import dash_auth
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import plotly
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
import os
import flask

#USERNAME_PASSWORD_PAIRS = [['prabal','prabal@123'],['arunima','arunima@123'],['intellispirit','123']]
STATIC_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),'assets')
df = pd.read_excel(STATIC_PATH+'/Book2.xlsx')
dfp=pd.read_excel(STATIC_PATH+'/Book1.xlsx')
df.replace("Set", 0, inplace=True)
app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP],meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])

server=app.server

#import os
#STATIC_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
#auth=dash_auth.BasicAuth(app,USERNAME_PASSWORD_PAIRS)


#replacable values as & when request given
District = 1
Zone_no = 1
School_no = 1

# subdf = df[(df['Distt']==District) & (df['Zone']==Zone_no) & (df['School']==School_no) & (df['Class']==10) & (df['Section']=='A')]
app.config['suppress_callback_exceptions'] = True


# **--------------------------------------app layout-----------------------------------**


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

#-------------Home Page-----------------
index_page = html.Div([
    html.H1("School's Dashboard", style={'text-align': 'center'}),
    # dcc.Link('Go to School Dasboard', href='/page-1'),
    dcc.Link('Go to Principal Dasboard', href='/school/1'),
    html.Br(),
    dcc.Link('Go to Teacher Dashboard', href='/teacher'),
], style = {'font-size': 'large'})


#-------------Page 1: Principal Dashboard(School Dasboard)--------------
newdf = dfp[(dfp['Distt'] == District) & (dfp['Zone'] == Zone_no)]
ndf = newdf[newdf['School'] == School_no]
opts = (ndf['Class'].unique()).tolist()
opts.insert(0, 'School')
page_1_layout = html.Div(
# app.layout = html.Div([
    children=[
    # dcc.Location(id='url', refresh=False),
    html.Div(id='test'),
    html.Div([
    html.Div([
    #filters
        html.Div([
            html.Div([

            html.Div([
                html.Label(["Choose Class"],style={'float':'left'}),
                html.Div([
                dcc.Dropdown(id='dd_pclass',clearable=False,style={'text-align':'left'},                
                    options = [{'label': i, 'value': i} for i in opts],
                    value = 'School'
                )
                ],style={'float':'right','width':'90px'}),
            ],className="col-sm-8",style={'margin-bottom':'10px',}),

            ],className="row", style={}),

            html.Div([
            html.Div([
                html.Label(["Choose Subject"],style={'float':'left'}),
                html.Div([
                dcc.Dropdown(id='dd_psub',clearable=False,style={'text-align':'left'},
                    options = [{'label': i, 'value': i} for i in ndf['Subject Category'].unique()],
                    value = ndf['Subject Category'].iloc[0]
                )
                ],style={'float':'right','width':'90px'}),
            ],className="col-sm-8",style={'margin-bottom':'10px'})
            ],className="row", style={}),
        ],className="col-lg-5",style={}),
        html.Div([],className="col-lg-2"),

     # avgs
        html.Div([
            html.Div([
            html.Div([
                    html.Div([
                    html.Div(html.P(id='pass'),className="row justify-content-sm-center",style={'font-size':'250%',"text-align":"center","justify-content":"center","align-items":"center"}),
                    html.Div(html.P('Pass Percentage'),className="row justify-content-sm-center",style={"text-align":"center","justify-content":"center","align-items":"center"}),
                    ],className="col-sm-4 ",style={"text-align":"center"}),

                    html.Div([
                    html.Div(html.P(id='pass90'),className="row justify-content-sm-center",style={'font-size':'250%',"text-align":"center","justify-content":"center","align-items":"center"}),
                    html.Div(html.P('Students above 90%'),className="row justify-content-sm-center",style={"text-align":"center","justify-content":"center","align-items":"center"}),
                    ],className="col-sm-4 ",style={"text-align":"center"}),

                    html.Div([
                    html.Div(html.P(id='pass75'),className="row justify-content-sm-center",style={'font-size':'250%',"text-align":"center","justify-content":"center","align-items":"center"}),
                    html.Div(html.P('Students above 75%'),className="row justify-content-sm-center",style={"text-align":"center","justify-content":"center","align-items":"center"}),
                    ],className="col-sm-4 ",style={"text-align":"center"}),

                    html.Div([
                    html.Div(html.P(id='fail'),className="row justify-content-sm-center",style={'font-size':'250%',"text-align":"center","justify-content":"center","align-items":"center"}),
                    html.Div(html.P('Students Failed'),className="row justify-content-sm-center",style={"text-align":"center","justify-content":"center","align-items":"center"}),
                    ],className="col-sm-4 ",style={"text-align":"center"}),

                    html.Div([
                    html.Div(html.P(id='fail1'),className="row justify-content-sm-center",style={'font-size':'250%',"text-align":"center","justify-content":"center","align-items":"center"}),
                    html.Div(html.P('Students failed in 1 Subject'),className="row justify-content-sm-center",style={"text-align":"center","justify-content":"center","align-items":"center"}),
                    ],className="col-sm-4 ",style={"text-align":"center"}),

                    html.Div([
                    html.Div(html.P(id='fail2'),className="row justify-content-sm-center",style={'font-size':'250%',"text-align":"center","justify-content":"center","align-items":"center"}),
                    html.Div(html.P('Students failed in 1 Subject'),className="row justify-content-sm-center",style={"text-align":"center","justify-content":"center","align-items":"center"}),
                    ],className="col-sm-4 ",style={"text-align":"center"}),

            ], className="row justify-content-xs-center",style={}),
            ],className="container"),
         ],className="col-lg-5",style={}),

    ],className="row", style={'margin-bottom':'10px','margin-top':'20px'}),
    ],className="container-fluid",style={'margin-bottom':'10px'}),

    # graphs
        html.Div([
        html.Div([
            # html.Div(className="col-lg-1",style={}),
            html.Div(dcc.Graph(id='class-wise-graph',config={"displaylogo": False,}), className="col-lg-6",style={}),
            html.Div(dcc.Graph(id='sub-teacher-wise-graph',config={"displaylogo": False,}),className="col-lg-6",style={}),
        ], className="row",style={'text-align':'center'}), ],className="container-fluid",),
    # html.Div(id='page-1-content'),
        html.Div([
            html.Br(),
            dcc.Link('Go to Teacher Dashboard', href='/teacher'),
            html.Br(),
            dcc.Link('Go back to home', href='/'),  
        ], style = {'font-size': 'large'})  

    ],style={'background-color': '#FFFFFF','width':'100%','text-align':'center'}  
)


# **--------------------------------------callbacks-----------------------------------**

@app.callback(
    Output('test','children'),
    [Input('url', 'pathname')]
)
# def update_test(selected_school):
    # ndf = newdf[newdf['School'] == int(selected_school[8:])]
    # opts = (ndf['Class'].unique()).tolist()
    # opts.insert(0, 'School')
    # return html.H2('School ' + selected_school[8:] + ' Dashboard')
# class dropdown
# @app.callback(
#     [Output('dd_pclass', 'options'),
#      Output('dd_pclass', 'value')],
#     [Input('url', 'pathname')]
# )
# def update_dd_pclass(selected_school):
#     ndf = newdf[newdf['School'] == int(selected_school[8:])]
#     opts = (ndf['Class'].unique()).tolist()
#     opts.insert(0, 'School')
#     options = [{'label': i, 'value': i} for i in opts]
#     value = 'School'
#     return options, value

# stickers
@app.callback(
    [Output('pass', 'children'),
     Output('pass90', 'children'),
     Output('pass75', 'children'),
     Output('fail', 'children'),
     Output('fail1', 'children'),
     Output('fail2', 'children'),
     ],
    [Input('url', 'pathname'),
     Input('dd_pclass', 'value')]
)
def update_your_avg(selected_school, selected_class):
    ndf = newdf[newdf['School'] == int(selected_school[8:])]

    if selected_class == 'School':

        subs = ndf['Subject Category'].unique()
        subs = sorted(subs)
        students = ndf['Student ID'].unique()

        percentage = []
        student_fail = []
        students_above_90 = 0
        students_above_75 = 0
        students_above_33 = 0
        students_fail_in_one_sub = 0
        students_fail_in_two_sub = 0
        students_fail = 0

        for i in range(len(students)):
            temp = 0
            fail_count = 0
            for j in range(len(subs)):
                temp += round(ndf[(ndf['Student ID'] == students[i]) & (
                    ndf['Subject Category'] == subs[j])]['Total Marks achieved'].mean())
                if((round(ndf[(ndf['Student ID'] == students[i]) & (ndf['Subject Category'] == subs[j])]['Total Marks achieved'].mean())) < 33):
                    fail_count = fail_count+1
            student_fail.append(fail_count)
            temp = ((temp/500))
            if(temp >= 0.9):
                students_above_90 = students_above_90+1
            if(temp > 0.75):
                students_above_75 = students_above_75+1
            percentage.append(temp)
        for i in range(0, len(student_fail)):
            if(student_fail[i] == 0):
                students_above_33 = students_above_33+1
            elif(student_fail[i] == 1):
                students_fail_in_one_sub = students_fail_in_one_sub+1
            elif(student_fail[i] == 2):
                students_fail_in_two_sub = students_fail_in_two_sub+1
            else:
                students_fail = students_fail+1

        pass_percentage = round((students_above_33/len(students)) * 100)

        return pass_percentage, students_above_90, students_above_75, students_fail, students_fail_in_one_sub, students_fail_in_two_sub

    else:
        ndf = ndf[ndf['Class'] == selected_class]
        subs = sorted(ndf['Subject Category'].unique())
        students = ndf['Student ID'].unique()
        percentage = []
        student_fail = []
        students_above_90 = 0
        students_above_75 = 0
        students_above_33 = 0
        students_fail_in_one_sub = 0
        students_fail_in_two_sub = 0
        students_fail = 0

        for i in range(len(students)):
            temp = 0
            fail_count = 0
            for j in range(len(subs)):
                temp += round(ndf[(ndf['Student ID'] == students[i]) & (
                    ndf['Subject Category'] == subs[j])]['Total Marks achieved'].mean())
                if(int(round(ndf[(ndf['Student ID'] == students[i]) & (ndf['Subject Category'] == subs[j])]['Total Marks achieved'].mean())) < 33):
                    fail_count = fail_count+1
            student_fail.append(fail_count)
            temp = ((temp/500))
            if(temp >= 0.9):
                students_above_90 = students_above_90+1
            if(temp > 0.75):
                students_above_75 = students_above_75+1
            percentage.append(temp)
        for i in range(0, len(student_fail)):
            if(student_fail[i] == 0):
                students_above_33 = students_above_33+1
            elif(student_fail[i] == 1):
                students_fail_in_one_sub = students_fail_in_one_sub+1
            elif(student_fail[i] == 2):
                students_fail_in_two_sub = students_fail_in_two_sub+1
            else:
                students_fail = students_fail+1

        pass_percentage = round((students_above_33/len(students)) * 100)

        return pass_percentage, students_above_90, students_above_75, students_fail, students_fail_in_one_sub, students_fail_in_two_sub


# class wise graph
@app.callback(
    Output('class-wise-graph', 'figure'),
    [Input('url', 'pathname'),
     Input('dd_pclass', 'value')]
)
def update_pgraph_1(selected_school, selected_class):
    ndf = newdf[newdf['School'] == int(selected_school[8:])]

    if selected_class == 'School':
        classes = ndf['Class'].unique()
        subs = sorted(ndf['Subject Category'].unique())
        score = []
        for i in range(len(classes)):
            score.append([])
            for j in range(len(subs)):
                score[i].append(int(round(ndf[(ndf['Class'] == classes[i]) & (
                    ndf['Subject Category'] == subs[j])]['Total Marks achieved'].mean())))

        x_axis = np.arange(1, 100)

        # graph
        figA = go.Figure()
        colour = ['#003f5c', '#374c80', '#7a5195']
        for i in range(len(score)):
            figA.add_trace(go.Bar(
                x=subs,
                y=score[i],
                name=str(classes[i]),
                text=score[i],
                textposition='outside',
                texttemplate='%{text}%',
                marker_color=colour[i],
                width=0.2
            ))

        figA.update_layout(barmode='group',
                           title='<b>School Performance</b>', title_x=0.5, title_y=0.9,
                           legend=dict(y=-0.1, x=0.3, font_size=10), legend_orientation="h",
                           xaxis=dict(showline=False,
                                      showgrid=False, zeroline=True,),
                           plot_bgcolor='white',
                           yaxis=dict(showgrid=True, gridcolor='#E5ECF6', showline=False, zeroline=True, range=[
                                      0, 100], nticks=20),
                           )
        return figA

    else:
        # new df containing data of particular class only
        cdf = ndf[ndf['Class'] == selected_class]

        # subs order in graph is diff. & here is same as order in spreadsheet
        subs = sorted(cdf['Subject Category'].unique())
        sections = cdf['Section'].unique()
        score = []
        for i in range(len(sections)):
            score.append([])
            for j in range(len(subs)):
                score[i].append(int(round(cdf[(cdf['Section'] == sections[i]) & (cdf['Subject Category'] == subs[j])]['Total Marks achieved'].mean())))

        x_axis = np.arange(1, 100)

        # graph
        figB = go.Figure()
        colour = ['#003f5c', '#374c80', '#7a5195', '#bc5090', '#ef5675']
        for i in range(len(score)):
            figB.add_trace(go.Bar(
                x=subs,
                y=score[i],
                name=str(sections[i]),
                text=score[i],
                textposition='outside',
                texttemplate='%{text}%',
                marker_color=colour[i],
                width=0.2
            ))

        figB.update_layout(barmode='group',
                           title='<b>Class </b>' + str(selected_class) + '<b> Performance</b>', title_x=0.5, title_y=0.9,
                           legend=dict(y=-0.1, x=0.3, font_size=10), legend_orientation="h",
                           xaxis=dict(showline=False,
                                      showgrid=False, zeroline=True,),
                           plot_bgcolor='white',
                           yaxis=dict(showgrid=True, gridcolor='#E5ECF6', showline=False, zeroline=True, range=[
                                      0, 100], nticks=20),
                           )
        return figB


# subject teacher wise
# subject dropdown
# @app.callback(
#     [Output('dd_psub', 'options'),
#      Output('dd_psub', 'value')],
#     [Input('url', 'pathname')]
# )
# def update_dd_psub(selected_school):
#     ndf = newdf[newdf['School'] == int(selected_school[8:])]
#     options = [{'label': i, 'value': i} for i in ndf['Subject Category'].unique()]
#     value = ndf['Subject Category'].iloc[0]
#     return options, value

# subject teacher wise graph


@app.callback(
    Output('sub-teacher-wise-graph', 'figure'),
    [Input('url', 'pathname'),
     Input('dd_psub', 'value')]
)
def update_pgraph_2(selected_school, selected_sub):
    ndf = newdf[newdf['School'] == int(selected_school[8:])]

    # df for selected subject only
    sdf = ndf[ndf['Subject Category'] == selected_sub]
    classes = sdf['Class'].unique()
    teachers = sdf['Teacher'].unique()
    score = []
    for i in range(len(teachers)):
        score.append([])
        for j in range(len(classes)):
            score[i].append(int(round(sdf[(sdf['Teacher'] == teachers[i]) & (sdf['Class'] == classes[j])]['Total Marks achieved'].mean())))

    x_axis = np.arange(1, 100)

    # graph
    figC = go.Figure()
    colour = ['#004c6d', '#6996b3', '#c1e7ff']
    for i in range(len(score)):
        figC.add_trace(go.Bar(
            x=classes,
            y=score[i],
            name=str(teachers[i]),
            text=score[i],
            textposition='outside',
            texttemplate='%{text}%',
            marker_color=colour[i],
            width=0.2
        ))

    figC.update_layout(barmode='group',
                       title=selected_sub + '<b> Teachers Performance</b>', title_x=0.5, title_y=0.9,
                       legend=dict(y=-0.1, x=0.3, font_size=10), legend_orientation="h",
                       xaxis=dict(showline=False, showgrid=False,
                                  zeroline=True,),
                       plot_bgcolor='white',
                       yaxis=dict(showgrid=True, gridcolor='#E5ECF6',
                                  showline=False, zeroline=True, range=[0, 100], nticks=20),
                       )
    return figC

# **------------------------------------------page 2: Teacher Dashboards-----------------------------------------------**
# subdf = df[(df['Distt']==District) & (df['Zone']==Zone_no) & (df['School']==School_no) & (df['Class']==10) & (df['Section']=='A')]

# page_2_layout = html.Div([
#     html.H1('Page 2'),
    
#     html.Br(),
#     dcc.Link('Go to Page 1', href='/school/1'),
#     html.Br(),
#     dcc.Link('Go back to home', href='/'),
# ])


page_2_layout = html.Div([
    # html.H1('Teacher Wise Stats', style={'text-align' : 'center'}),
    html.Div(
    children=[
            
    html.Div([
    #filters
        html.Div([

            html.Div([
                html.Label(["Choose Teacher"],style={'float':'left'}),
                html.Div([
                dcc.Dropdown( id='dd_teacher',clearable=False,style={'text-align':'left'},
                    options=[{'label': i, 'value': i} for i in df[(df['Distt']==District) & (df['Zone']==Zone_no) & (df['School']==School_no)]['Teacher'].unique()],
                    value=df[(df['Distt']==District) & (df['Zone']==Zone_no) & (df['School']==School_no)]['Teacher'].iloc[0])],style={'float':'right'}),
            ],style={'width': '40%','display':'inline-block','margin-left':'5%','margin-right':'5%','margin-bottom':'2%'}),
            html.Div([
                html.Label(["Choose Class"],style={'float':'left'}),
                html.Div([
                dcc.Dropdown(id='dd_class',clearable=False,style={'text-align':'left'},)],style={'float':'right'}),
            ],style={'width': '40%','display':'inline-block','margin-left':'5%','margin-right':'5%','margin-bottom':'2%'}),
            html.Div([
                html.Label(["Choose Section"],style={'float':'left'}),
                html.Div([
                dcc.Dropdown(id='dd_section',clearable=False,style={'text-align':'left'},)],style={'float':'right'}),
            ],style={'width': '40%','display':'inline-block','margin-left':'5%','margin-right':'5%','margin-bottom':'2%'}),
            html.Div([  
                html.Label(["Choose Subject"],style={'float':'left'}),
                html.Div([
                dcc.Dropdown(id='dd_sub',clearable=False,style={'text-align':'left'},)],style={'float':'right'}),
            ],style={'width': '40%','display':'inline-block','margin-left':'5%','margin-right':'5%','margin-bottom':'2%'})
        ],style={'float':'left', 'width':'35%'}),

     # avgs
        html.Div([ 
            html.Div([
                html.Div(html.P(id='your-avg'),style={'display':'inline-block','font-size':'250%'}),
                html.Div(html.P(id='school-avg'),style={'display':'inline-block','font-size':'250%','margin-left':'13%','margin-right':'13%'}),
                html.Div(html.P(id='distt-avg'),style={'display':'inline-block','font-size':'250%'})
            ], className="row",style={}),
            html.Div([
                html.Div(html.P('Class Average'),style={'display':'inline-block','width':'20%'}),
                html.Div(html.P('School Average'),style={'display':'inline-block','width':'20%'}),
                html.Div(html.P('District Average'),style={'display':'inline-block','width':'20%'})
            ], className="row",style={})
         ],style={'width': '40%','text-align':'center','align-items':'center','float':'right'}),
    ], style={'margin-bottom':'5px','margin-top':'20px','width':'100%','display':'inline-block'}),

    # tabs
       html.Div([
            #html.Label(["CHOOSE TOPIC"]),
            dcc.Tabs(id='tabs-example',
           
            colors={"border": "white","primary": "#C9DDF2","background": "#EAF2FA"}
            ),
            ],style={'display':'inline-block','width': '40%','margin-bottom':'10px',}
            ),

    # graphs
        html.Div([
            html.Div(dcc.Graph(id='dtt-avg-scatter',config={"displaylogo": False,}), style={'display':'inline-block','width': '31%', }),
            html.Div(dcc.Graph(id='pie-graph',config={"displaylogo": False,}),style={'display':'inline-block','width': '31%','text-align': 'center', 'margin-left':'13px'}),
            html.Div(dcc.Graph(id='topic-wise-performance',config={"displaylogo": False,}),style={'display':'inline-block','width': '31%','text-align': 'center','background-color':'white','margin-left':'13px'}),
        ], className="row"),

        html.Div([
            html.Br(),
            dcc.Link('Go to Principal dashboard', href='/school/1'),
            html.Br(),
            dcc.Link('Go back to home', href='/'),
        ],style={'font-size':'large'}
        )

    ],style={'background-color': '#FFFFFF','width':'100%','text-align':'center'})    
])

if __name__ == '__main__':
    app.run_server(debug=True)
