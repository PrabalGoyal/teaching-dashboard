import flask
from flask import request
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import plotly
import plotly.graph_objs as go
import dash_bootstrap_components as dbc

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

server = flask.Flask(__name__)
app = dash.Dash(__name__, server = server, routes_pathname_prefix='/', external_stylesheets=external_stylesheets)

@server.route('/teacher/<selected_teacher>/')
def my_function(selected_teacher):
    df = pd.read_excel(r'Data.xlsx')
    df.replace("Set", 0, inplace=True)

    #replacable values as & when request given
    District = 1
    Zone_no = 1
    School_no = 1
    # Teacher_no = 1

    #subdf = df[(df['Distt']==District) & (df['Zone']==Zone_no) & (df['School']==School_no) & (df['Class']==10) & (df['Section']=='A')]
    # app.config['suppress_callback_exceptions'] = True
    # **--------------------------------------app layout-----------------------------------**
    selected_teacher = str(selected_teacher)
    print(selected_teacher)
    selected_teacher=int(selected_teacher)
    app.layout = html.Div(
        children=[
            html.H1(
        children=selected_teacher
    ),
        html.Div([
            html.Div([

                # html.Div([
                #     html.Label(["Choose Teacher"],style={'float':'left'}),
                #     html.Div([
                #     dcc.Dropdown( id='dd_teacher',clearable=False,style={'text-align':'left'},
                #         options=[{'label': i, 'value': i} for i in df[(df['Distt']==District) & (df['Zone']==Zone_no) & (df['School']==School_no)]['Teacher'].unique()],
                #         disabled=True,
                #         value=df[(df['Distt']==District) & (df['Zone']==Zone_no) & (df['School']==School_no)]['Teacher'].iloc[0])],style={'float':'right'}),
                # ],style={'width': '40%','display':'inline-block','margin-left':'5%','margin-right':'5%','margin-bottom':'2%'}),
                html.Div([
                    html.Label(["Choose Class"],style={'float':'left'}),
                    html.Div([
                    dcc.Dropdown(id='dd_class',clearable=False,style={'text-align':'left'},

                    options = [{'label': i, 'value': i} for i in df[(df['Distt']==District) & (df['Zone']==Zone_no) & (df['School']==School_no) & (df['Teacher']==selected_teacher)]['Class'].unique()],
                    value=df[(df['Distt']==District) & (df['Zone']==Zone_no) & (df['School']==School_no) & (df['Teacher']==int(selected_teacher))]['Class'].iloc[0])], style={'float':'right'}),
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

        #graphs
            html.Div([
                html.Div(dcc.Graph(id='dtt-avg-scatter',config={"displaylogo": False,}), style={'display':'inline-block','width': '31%', }),
                html.Div(dcc.Graph(id='pie-graph',config={"displaylogo": False,}),style={'display':'inline-block','width': '31%','text-align': 'center', 'margin-left':'13px'}),
                html.Div(dcc.Graph(id='topic-wise-performance',config={"displaylogo": False,}),style={'display':'inline-block','width': '31%','text-align': 'center','background-color':'white','margin-left':'13px'}),
            ], className="row"),

        ],style={'background-color': '#FFFFFF','width':'100%','text-align':'center'})

    # **------------------------------------------callbacks-----------------------------------------------**

    # ----------------dropdowns-----------

    #callback for class dropdown
    # @app.callback(
    #     [Output('dd_class', 'options'),
    #     Output('dd_class', 'value')],
    #     [Input('dd_teacher', 'value')]
    #     )    
    # def update_dd_class():
    #     options = [{'label': i, 'value': i} for i in df[(df['Distt']==District) & (df['Zone']==Zone_no) & (df['School']==School_no) & (df['Teacher']==selected_teacher)]['Class'].unique()]
    #     value=df[(df['Distt']==District) & (df['Zone']==Zone_no) & (df['School']==School_no) & (df['Teacher']==selected_teacher)]['Class'].iloc[0]
    #     return options,value

    #callback for section dropdown
    # @app.callback(
    #     [Output('dd_section', 'options'),
    #     Output('dd_section', 'value')
    #     ],
    #     [
    #     # Input('dd_teacher', 'value'),
    #     Input('dd_class', 'value')]
    #     )    
    # def update_dd_section(selected_class):
    #     options = [{'label': i, 'value': i} for i in df[(df['Distt']==District) & (df['Zone']==Zone_no) & (df['School']==School_no) & (df['Teacher']==selected_teacher) & (df['Class']==selected_class)]['Section'].unique()]
    #     value = df[(df['Distt']==District) & (df['Zone']==Zone_no) & (df['School']==School_no) & (df['Teacher']==selected_teacher) & (df['Class']==selected_class)]['Section'].iloc[0]
    #     return options, value

    #callback for subject dropdown
    @app.callback(
        [Output('dd_sub', 'options'),
        Output('dd_sub', 'value')],
        [
        # Input('dd_teacher', 'value'),
        Input('dd_class', 'value'),
        Input('dd_section', 'value')])    
    def update_dd_sub(selected_class, selected_section):
        options = [{'label': i, 'value': i} for i in df[(df['Distt']==District) & (df['Zone']==Zone_no) & (df['School']==School_no) & (df['Teacher']==selected_teacher) & (df['Class']==selected_class) & (df['Section']==selected_section)]['Subject Category'].unique()]
        value = df[(df['Distt']==District) & (df['Zone']==Zone_no) & (df['School']==School_no) & (df['Teacher']==selected_teacher) & (df['Class']==selected_class) & (df['Section']==selected_section)]['Subject Category'].iloc[0]
        return options, value

    #------------------------------------averages-----------------------------------------
        
    #3 avg values
    @app.callback(
        Output('your-avg', 'children'),
        [
            # Input('dd_teacher', 'value'),
        Input('dd_class', 'value'),
        Input('dd_section', 'value'),
        Input('dd_sub', 'value')]
        )
    def update_your_avg(selected_class, selected_section, selected_sub):
        return round(df[(df['Distt']==District) & (df['Zone']==Zone_no) & (df['School']==School_no) &  (df['Teacher']==selected_teacher) & (df['Class']==selected_class) & (df['Section']==selected_section) & (df['Subject Category']==selected_sub)]['Total'].mean())

    @app.callback(
        Output('school-avg', 'children'),
        [
            # Input('dd_teacher', 'value'),
        Input('dd_class', 'value'),
        Input('dd_section', 'value'),
        Input('dd_sub', 'value')]
        )
    def update_school_avg(selected_class, selected_section, selected_sub):
        return round(df[(df['Distt']==District) & (df['Zone']==Zone_no) &  (df['School']==School_no) & (df['Class']==selected_class) & (df['Subject Category']==selected_sub)]['Total'].mean())

    @app.callback(
        Output('distt-avg', 'children'),
        [
            # Input('dd_teacher', 'value'),
        Input('dd_class', 'value'),
        Input('dd_section', 'value'),
        Input('dd_sub', 'value')]
        )
    def update_distt_avg(selected_class, selected_section, selected_sub):
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
        [
            # Input('dd_teacher', 'value'),
        Input('dd_class', 'value'),
        Input('dd_section', 'value'),
        Input('dd_sub', 'value'),
        Input('tabs-example', 'value')]
        )
    def update_graph_1(selected_class, selected_section, selected_sub, selected_sub_slider):
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
    # Input('dd_teacher', 'value'),
    Input('dd_class', 'value'),
    Input('dd_section', 'value')]
    )
    def update_graph_5(selected_sub_slider, selected_sub, selected_class, selected_section):

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
    # Input('dd_teacher', 'value'),
    Input('dd_class', 'value'),
    Input('dd_section', 'value'),
    Input('dd_sub', 'value')]
    )

    def update_graph_6(selected_sub_slider, selected_class, selected_section, selected_sub):

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
    return app.index()       

app.layout = html.Div(style={}, children=[
    html.H1(
        children='HOME'
    )
])
if __name__ == '__main__':
    app.run_server(debug=True)