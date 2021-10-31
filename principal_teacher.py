# **-------------------------------------- importing libraries -----------------------------------**
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
import plotly
import plotly.graph_objs as go
import dash_bootstrap_components as dbc

# **--------------------------------------global declarations-----------------------------------**

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', dbc.themes.BOOTSTRAP]
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#* To Do : change /school/ to /school/
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])

#reading principal dashboard data
dfp = pd.read_excel('Book1.xlsx')

#reading teacher dashboard data
df = pd.read_excel('Book2.xlsx')
df.replace("Set", 0, inplace=True)

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
                    html.Div(html.P('Students failed in 2 Subject'),className="row justify-content-sm-center",style={"text-align":"center","justify-content":"center","align-items":"center"}),
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
            dcc.Link('Go to Page 2', href='/teacher'),
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
def update_test(selected_school):
    # ndf = newdf[newdf['School'] == int(selected_school[8:])]
    # opts = (ndf['Class'].unique()).tolist()
    # opts.insert(0, 'School')
    return html.H2('School ' + selected_school[8:] + ' Dashboard')
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
    html.H1('Teacher Wise Stats', style={'text-align' : 'center'}),
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
            dcc.Link('Go to Page 1', href='/school/1'),
            html.Br(),
            dcc.Link('Go back to home', href='/'),
        ],style={'font-size':'large'}
        )

    ],style={'background-color': '#FFFFFF','width':'100%','text-align':'center'})    
])

#----------------dropdowns-----------

#callback for class dropdown
@app.callback(
    [Output('dd_class', 'options'),
    Output('dd_class', 'value')],
    [Input('dd_teacher', 'value')]
    )    
def update_dd1_class(selected_teacher):
    options = [{'label': i, 'value': i} for i in df[(df['Distt']==District) & (df['Zone']==Zone_no) & (df['School']==School_no) & (df['Teacher']==selected_teacher)]['Class'].unique()]
    value=df[(df['Distt']==District) & (df['Zone']==Zone_no) & (df['School']==School_no) & (df['Teacher']==selected_teacher)]['Class'].iloc[0]
    return options,value

#callback for section dropdown
@app.callback(
    [Output('dd_section', 'options'),
    Output('dd_section', 'value')],
    [Input('dd_teacher', 'value'),
    Input('dd_class', 'value')]
    )    
def update_dd_section(selected_teacher, selected_class):
    options = [{'label': i, 'value': i} for i in df[(df['Distt']==District) & (df['Zone']==Zone_no) & (df['School']==School_no) & (df['Teacher']==selected_teacher) & (df['Class']==selected_class)]['Section'].unique()]
    value = df[(df['Distt']==District) & (df['Zone']==Zone_no) & (df['School']==School_no) & (df['Teacher']==selected_teacher) & (df['Class']==selected_class)]['Section'].iloc[0]
    return options, value

#callback for subject dropdown
@app.callback(
    [Output('dd_sub', 'options'),
    Output('dd_sub', 'value')],
    [Input('dd_teacher', 'value'),
    Input('dd_class', 'value'),
     Input('dd_section', 'value')])    
def update_dd_sub(selected_teacher, selected_class, selected_section):
    options = [{'label': i, 'value': i} for i in df[(df['Distt']==District) & (df['Zone']==Zone_no) & (df['School']==School_no) & (df['Teacher']==selected_teacher) & (df['Class']==selected_class) & (df['Section']==selected_section)]['Subject Category'].unique()]
    value = df[(df['Distt']==District) & (df['Zone']==Zone_no) & (df['School']==School_no) & (df['Teacher']==selected_teacher) & (df['Class']==selected_class) & (df['Section']==selected_section)]['Subject Category'].iloc[0]
    return options, value

#------------------------------------averages-----------------------------------------
    
#3 avg values
@app.callback(
    Output('your-avg', 'children'),
    [Input('dd_teacher', 'value'),
    Input('dd_class', 'value'),
     Input('dd_section', 'value'),
     Input('dd_sub', 'value')]
    )
def update_avg(selected_teacher, selected_class, selected_section, selected_sub):
    return round(df[(df['Distt']==District) & (df['Zone']==Zone_no) & (df['School']==School_no) &  (df['Teacher']==selected_teacher) & (df['Class']==selected_class) & (df['Section']==selected_section) & (df['Subject Category']==selected_sub)]['Total'].mean())

@app.callback(
    Output('school-avg', 'children'),
    [Input('dd_teacher', 'value'),
    Input('dd_class', 'value'),
     Input('dd_section', 'value'),
     Input('dd_sub', 'value')]
    )
def update_school_avg(selected_teacher, selected_class, selected_section, selected_sub):
    return round(df[(df['Distt']==District) & (df['Zone']==Zone_no) &  (df['School']==School_no) & (df['Class']==selected_class) & (df['Subject Category']==selected_sub)]['Total'].mean())

@app.callback(
    Output('distt-avg', 'children'),
    [Input('dd_teacher', 'value'),
    Input('dd_class', 'value'),
     Input('dd_section', 'value'),
     Input('dd_sub', 'value')]
    )
def update_distt_avg(selected_teacher, selected_class, selected_section, selected_sub):
    return round(df[(df['Distt']==District) & (df['Class']==selected_class) & (df['Subject Category']==selected_sub)]['Total'].mean())
    
#avgs colour logic
#callback for your average colour
@app.callback(
    Output('your-avg', 'style'),
    [Input('your-avg', 'children'),
    Input('school-avg', 'children'),
    Input('distt-avg', 'children')]
    )
def colour_your_avg(your_avg, school_avg, distt_avg):
    if your_avg < school_avg and your_avg < distt_avg:
        colour = '#ce0c0c'
    elif your_avg < school_avg or your_avg < distt_avg:
        colour = '#feb204'
    else:
        colour = '#109e0e'
    return {'color' : colour}

#callback for school average colour
@app.callback(
    Output('school-avg', 'style'),
    [Input('school-avg', 'children'),
    Input('distt-avg', 'children')]
    )
def colour_school_avg(school_avg, distt_avg):
    if school_avg < distt_avg:
        colour = '#ce0c0c'
    else:
        colour = '#109e0e'
    return {'color' : colour}

#------------------------------------tabs-----------------------------------------

#callback sets no .of tabs
    # code will have to change when parsing pattern changes
@app.callback(
    [Output('tabs-example', 'children'),
    Output('tabs-example', 'value')],
    [Input('dd_sub', 'value')]
    )
    
def update_nooftabs(selected_sub):
    # generate Topics[] based on dd_sub
    Topics = [idx for idx in df.columns if idx.startswith('Topic ')]
    Topics.insert(0, 'All')
    tabs_list = []
    for i in Topics:
        tabs_list.append(dcc.Tab(label=i, value=i))    
    value = Topics[0]
    return tabs_list, value
  
#------------------------------------graphs-----------------------------------------
#updates graph 1 (dtt-avg-scatter graph)
@app.callback(
    Output('dtt-avg-scatter', 'figure'),
    [Input('dd_teacher', 'value'),
    Input('dd_class', 'value'),
     Input('dd_section', 'value'),
     Input('dd_sub', 'value'),
     Input('tabs-example', 'value')]
    )
def update_graph1(selected_teacher, selected_class, selected_section, selected_sub, selected_sub_slider):
    if selected_sub_slider == 'All':
        District_Average = round(df[(df['Distt']==District) & (df['Class']==selected_class) & (df['Subject Category']==selected_sub)]['Total'].mean())
        School_Average = round(df[(df['Distt']==District) & (df['Zone']==Zone_no) & (df['School']==School_no) &  (df['Subject Category']==selected_sub)]['Total'].mean())
        score_df = df[(df['Distt']==District) & (df['Zone']==Zone_no) & (df['School']==School_no) & (df['Class']==selected_class) & (df['Section']==selected_section) & (df['Subject Category']==selected_sub)]
        Score = np.array(score_df['Total'])
        no_of_students=(df[(df['Distt']==District) & (df['Zone']==Zone_no) & (df['School']==School_no) & (df['Class']==selected_class) & (df['Section']==selected_section) & (df['Subject Category']==selected_sub)].count()[0])+1
        x_axis= np.arange(1,no_of_students)
        District_Average=np.ones(no_of_students)*District_Average
        School_Average=np.ones(no_of_students)*School_Average

        #GRAPH A
        figA = go.Figure()

        figA.add_trace(go.Scatter(
            x=x_axis, y=District_Average,
            name='Distt_Average',
            mode='lines',
            line=dict(color='#838EDE', width=3)
        ))
        figA.add_trace(go.Scatter(
            x=x_axis, y=School_Average,
            name='School_Average',
            mode='lines',
            line=dict(color='#84C0D4', width=3)
        ))
        figA.add_trace(go.Scatter(
            x=x_axis, y=Score,
            name = 'Score',    
            mode='markers',
            marker=dict(color='#00688B',size=12,)
        ))

        figA.update_layout(title='<b>Class Distribution</b>', title_x=0.5, title_y=0.9,
                        xaxis_title='Number Of Student',
                        yaxis_title='Total Score',
                        legend=dict(y=-0.2,x=-0.04, traceorder='reversed', font_size=10),legend_orientation="h",
                        xaxis=dict(showline=False,showgrid=False,linecolor='rgb(0, 0, 0)',linewidth=2,nticks=10,zeroline=True,range=[0, no_of_students]),
                        yaxis=dict(showgrid=True,showline=False,gridcolor='#E5ECF6',linecolor='rgb(0, 0, 0)',linewidth=2,zeroline=True,range=[0,100],nticks=20),   
                        plot_bgcolor='white'                  
                        )
        return figA

    else:
        score_df = df[(df['Distt']==District) & (df['Zone']==Zone_no) & (df['School']==School_no) & (df['Class']==selected_class) & (df['Section']==selected_section) & (df['Subject Category']==selected_sub)]
        District_Average = score_df[selected_sub_slider].mean()
        School_Average = df[(df['Distt']==District) & (df['Zone']==Zone_no) & (df['Subject Category']==selected_sub)][selected_sub_slider].mean()
        Score = np.array(score_df[selected_sub_slider])
        no_of_students=(score_df.count()[0])+1
        x_axis= np.arange(1,no_of_students)
        District_Average=np.ones(no_of_students)*District_Average
        School_Average=np.ones(no_of_students)*School_Average

        #GRAPH A
        figA = go.Figure()

        figA.add_trace(go.Scatter(
            x=x_axis, y=District_Average,
            name='Distt_Average',
            mode='lines',
            line=dict(color='#838EDE', width=3)
        ))
        figA.add_trace(go.Scatter(
            x=x_axis, y=School_Average,
            name='School_Average',
            mode='lines',
            line=dict(color='#84C0D4', width=3)
        ))
        figA.add_trace(go.Scatter(
            x=x_axis, y=Score,
            name = 'Score',    
            mode='markers',
            marker=dict(color='#00688B',size=12,)
        ))

        figA.update_layout(title='<b>Class Distribution</b>', title_x=0.5, title_y=0.9,
                        xaxis_title='Number Of Students',
                        yaxis_title=selected_sub_slider + ' Score',
                        legend=dict(y=-0.2,x=-0.04, traceorder='reversed', font_size=10),legend_orientation="h",
                        xaxis=dict(showline=False,showgrid=False,linecolor='rgb(0, 0, 0)',linewidth=2,nticks=10,zeroline=True,range=[0, no_of_students]),
                        yaxis=dict(showgrid=True,showline=False,gridcolor='#E5ECF6',linecolor='rgb(0, 0, 0)',linewidth=2,zeroline=True,range=[0,(df[df['Subject Category'] == selected_sub][selected_sub_slider].iloc[0])+1],nticks=10),   
                        plot_bgcolor='white'                  
                        )
        return figA

#updates graph 2 (topic/subtopic importance pie graph )  
@app.callback(
Output('pie-graph', 'figure'),
[Input('tabs-example', 'value'),
Input('dd_sub', 'value'),
Input('dd_teacher', 'value'),
Input('dd_class', 'value'),
Input('dd_section', 'value')]
)
def update_graph_5(selected_sub_slider, selected_sub, selected_teacher, selected_class, selected_section):

    if selected_sub_slider == 'All':
        filtered_df = df[df['Subject Category'] == selected_sub]
        labels = [idx for idx in df.columns if idx.startswith('Topic ')]
        values=[]
        colors = ['#C4C4E7', '#9EB9DF', '#DDA8DD', '#E697BB','#DDE2E9']
        for i in range(len(labels)):
            values.append(filtered_df[labels[i]].iloc[0])
        traces=go.Pie(labels=labels, values=values, textinfo='label+percent',hole=0.2, insidetextorientation='radial',sort=True,hoverinfo='label+percent',textfont_size=10,marker=dict(colors=colors, line=dict(color='#000000', width=2)))
        return {
            'data' : [traces],
            'layout' : go.Layout(
                title='<b>Topic Importance</b>', title_x=0.5, title_y=0.9,showlegend=False,
            )
            } 


    else:
        labels = [idx for idx in df.columns if idx.startswith('Subtopic '+ selected_sub_slider[len('Topic '):])]
        values=[]
        colors = ['#C4C4E7', '#9EB9DF', '#DDA8DD', '#E697BB','#DDE2E9']
        for i in range(len(labels)):
            values.append(df[labels[i]][0])
        traces=go.Pie(labels=labels, values=values, textinfo='label+percent',hole=0.2, insidetextorientation='radial',sort=True,hoverinfo='label+percent',textfont_size=10,marker=dict(colors=colors, line=dict(color='#000000', width=2)))
        return {
            'data' : [traces],
            'layout' : go.Layout(
                title='<b>Subtopic Importance</b>', title_x=0.5, title_y=0.9,showlegend=False,
            )
            } 


#updates graph 3 (topic wise performance graph)
@app.callback(
Output('topic-wise-performance', 'figure'),
[Input('tabs-example', 'value'),
Input('dd_teacher', 'value'),
Input('dd_class', 'value'),
Input('dd_section', 'value'),
Input('dd_sub', 'value')]
)

def update_graph_6(selected_sub_slider, selected_teacher, selected_class, selected_section, selected_sub):

    if selected_sub_slider == 'All':
        Topics = [idx for idx in df.columns if idx.startswith('Topic ')]
        values=[]
        for i in range(len(Topics)):
            values.append(df[Topics[i]][0])
        
        topic_percent=[]
        for i in range(len(Topics)):
            topic_percent.append(df[(df['Distt']==District) & (df['Zone']==Zone_no) & (df['School']==School_no) & (df['Teacher']==selected_teacher)  & (df['Class']==selected_class) & (df['Section']==selected_section) & (df['Subject Category']==selected_sub)][Topics[i]].mean())
            topic_percent[i]=int(round((topic_percent[i]/values[i])*100))
        
        #District average calculation; stored in Distt_Average_array
        Distt_Average_array=[]
        for i in range(len(Topics)):
            Distt_Average_array.append((df[(df['Distt']==District) & (df['Class']==selected_class) & (df['Subject Category']==selected_sub)][Topics[i]].mean()))
            Distt_Average_array[i] = int(round((Distt_Average_array[i]/values[i])*100))

        colour = ['#AABBDE'] * len(topic_percent)
        for i in range(len(topic_percent)):
            if topic_percent[i] < Distt_Average_array[i]:
                colour[i] = '#DD3131'


        #GRAPH C
        figC = go.Figure()
        figC.add_trace(go.Bar(
            x=Topics,
            y=topic_percent,
            name='Your Class',
            text=topic_percent,
            textposition='outside',
            texttemplate='%{text}%',            
            marker_color = colour,
            width=0.3
        ))
        figC.add_trace(go.Bar(
            x=Topics,
            y=Distt_Average_array,
            texttemplate='%{text}%',
            name='Distt Average',
            text=Distt_Average_array,
            textposition='outside',
            marker_color='#3A5894',
            width=0.3

        ))

        figC.update_layout(barmode='group',
                            title='<b>Topic Wise Performance</b>', title_x=0.5, title_y=0.9,
                            legend=dict(y=-0.1,x=0.15, font_size=10),legend_orientation="h",
                            xaxis=dict(showline=False,showgrid=False,zeroline=True,),  
                            plot_bgcolor='white',                
                            yaxis=dict(showgrid=True,gridcolor='#E5ECF6',showline=False,zeroline=True,ticksuffix ='%',range=[0,100],nticks=20),   
                            )
        return figC

    else:

        labels = [idx for idx in df.columns if idx.startswith('Subtopic '+ selected_sub_slider[len('Topic '):])]
        values=[]
        for i in range(len(labels)):
            values.append(df[labels[i]][0])
        # Topics=[idx for idx in df.columns if idx.startswith('Subtopic '+str(selected_sub_slider))]
        subtopic_percent=[]
        for i in range(len(labels)):
            subtopic_percent.append(df[(df['Distt']==District) & (df['Zone']==Zone_no) & (df['School']==School_no) & (df['Teacher']==selected_teacher) & (df['Class']==selected_class) & (df['Section']==selected_section) & (df['Subject Category']==selected_sub)][labels[i]].mean())
            subtopic_percent[i]=int(round((subtopic_percent[i]/values[i])*100))
        
        Distt_Average_array=[]
        for i in range(len(labels)):
            Distt_Average_array.append((df[(df['Distt']==District) & (df['Class']==selected_class) & (df['Subject Category']==selected_sub)][labels[i]].mean()))
            Distt_Average_array[i] = int(round((Distt_Average_array[i]/values[i])*100))

        colour = ['#AABBDE'] * len(subtopic_percent)
        for i in range(len(subtopic_percent)):
            if subtopic_percent[i] < Distt_Average_array[i]:
                colour[i] = '#DD3131'
        

        figC = go.Figure()
        figC.add_trace(go.Bar(
            x=labels,
            y=subtopic_percent,
            name='Your Class',
            text=subtopic_percent,
            textposition='outside',
            texttemplate='%{text}%',
            marker_color = colour,
            width=0.3
        ))
        figC.add_trace(go.Bar(
            x=labels,
            y=Distt_Average_array,
            name='Distt Average',
            text=Distt_Average_array,
            texttemplate='%{text}%',
            textposition='outside',
            marker_color='#3A5894',
            width=0.3

        ))

        figC.update_layout(barmode='group',
                            title='<b>Subtopic Wise Performance</b>', title_x=0.5, title_y=0.9,
                            legend=dict(y=-0.1,x=0.15, font_size=10,),legend_orientation="h",
                            xaxis=dict(showline=False,showgrid=False,tickfont=dict(size=9),), 
                            plot_bgcolor='white',                 
                            yaxis=dict(showgrid=True,gridcolor='#E5ECF6',showline=False,zeroline=True,ticksuffix ='%',range=[0,100],nticks=20),   
                            )               
        return figC


# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/school/1':
        return page_1_layout
    elif pathname == '/teacher':
        return page_2_layout
    else:
        return index_page
    # Can also return a 404 "URL not found" page here


if __name__ == '__main__':
    app.run_server(debug=True)
