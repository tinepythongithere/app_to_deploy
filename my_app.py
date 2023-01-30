from dash import Dash, html, dcc
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import pandas as pd
from dash.dependencies import Input, Output
import dash_daq as daq

df = pd.read_csv("data/players_21.csv")
#============================================================
name = df.loc[:,'short_name']

#============================================================
name_players_1 = dcc.Dropdown(
    options=[
        {'label': i, 'value': i} for i in name
    ],
    #multi=True,
    value=name[0],
    id= 'name_player_1',
    #style={'width':'65%'}
)

name_players_2 = dcc.Dropdown(
    options=[
        {'label': i, 'value': i} for i in name
    ],
    #multi=True,
    value=name[1],
    id= 'name_player_2',
    #style={'width':'65%'}
)
#============================================================

nav_bar = dbc.Nav(
            [
                dbc.NavLink("Fiche personnelle", href="/fiche_perso", active="exact", style={'color': 'blue'}),
                dbc.NavLink("Comparaisons entre deux joureurs", href="/compar_2_players", active="exact", style={'color': 'blue'}),
                dbc.CardImg(src='assets/ball.jpg', style={"height":'2%', 'width':'2%'})
            ],
            pills=True,
            style={'border':'solid'}
        )

app = Dash(external_stylesheets=[dbc.themes.MATERIA])

page_compar = html.Div([
    html.H1("Players comparison", style={'text-align':'center', 'color':'blue', 'margin':'30px'}),
    dbc.Row([
        dbc.Col([
            dbc.Row(dbc.Card(
                dbc.CardBody([
                    html.Label('Player 1'),
                    name_players_1
                ], style={'text-align':'center'})
            )),
            dbc.Row(html.Img(src="assets\player_1.png"))
        ], width={'size':3, 'offset':1}),

        dbc.Col(dcc.Graph(id='polar_plot'), width=4),

        dbc.Col([
            dbc.Row(dbc.Card(
                dbc.CardBody([
                    html.Label('Player 2'),
                    name_players_2
                ], style={'text-align': 'center'})
            )),
            dbc.Row(html.Img(src="assets\player_3.png"))
        ], width=3)
    ], style={"margin-right": '12px'}),
    dbc.Row([
        dbc.Col(dcc.Graph(id="perform_player1"), width={'size':5, 'offset':1}),
        dbc.Col(dcc.Graph(id="perform_player2"), width=5)
    ], style={"margin-right": '12px'})

])

page_fiche_perso = html.Div([
    html.H1("Fiche personnelle", style={'text-align':'center', 'color':'blue', 'margin':'30px'}),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardImg(src="https://bootdey.com/img/Content/avatar/avatar7.png",
                            style={"height":'50', 'width':'50%', 'border-radius': '50%'}),
                html.Label("Short Name ..."),
                html.Label("Nationalité"),
                html.Label("Pieds Fort")
            ], style={'display':'flex','align-items':'center'})
        ], width={'size':3, 'offset':1}),
        dbc.Col([
            dbc.Card([
                html.Label("Long name"),
                html.Hr(),
                html.Label("Club actuel"),
                html.Hr(),
                html.Label("Poids"),
                html.Hr(),
                html.Label("Taille"),
                html.Hr(),
                html.Label("Valeur (en £)")
            ], style={'padding':'15px'})
        ], width=6),
    ]),
    html.Label(""),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                daq.Slider(
                    min=0,
                    max=100,
                    value=30,
                    disabled=True,
                    handleLabel={"showCurrentValue": True,"label": "Potential"},
                ),
                html.Br(),
                daq.Slider(
                    min=0,
                    max=5,
                    value=3,
                    disabled=True,
                    handleLabel={"showCurrentValue": True,"label": "Reputation"},
                ),
                html.Br(),
                daq.Slider(
                    min=0,
                    max=100,
                    value=30,
                    disabled=True,
                    handleLabel={"showCurrentValue": True,"label": "Pace"},
                ),
                html.Br(),
                daq.Slider(
                    min=0,
                    max=100,
                    value=20,
                    disabled=True,
                    handleLabel={"showCurrentValue": True,"label": "Shooting"},
                ),
                html.Br(),
                daq.Slider(
                    min=0,
                    max=100,
                    value=70,
                    disabled=True,
                    handleLabel={"showCurrentValue": True,"label": "Dribbling"},
                ),
                html.Br(),
                daq.Slider(
                    min=0,
                    max=100,
                    value=38,
                    disabled=True,
                    handleLabel={"showCurrentValue": True,"label": "Physic"}),
                html.Br(),
                daq.Slider(
                    min=0,
                    max=100,
                    value=58,
                    color='red',
                    disabled=True,
                    handleLabel={"showCurrentValue": True,"label": "Defending"},
                ),
            ], style={'padding':'15px'})
        ], width={'size':4, 'offset':4}),
    ])

])

content = html.Div(id="page-content", children=[page_compar])

app.layout = html.Div([
    dcc.Location(id="url"),
    nav_bar,
    content
])

@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def page_render(path):
    if path=="/fiche_perso":
        return page_fiche_perso
    elif path=="/compar_2_players":
        return page_compar

@app.callback(
    Output(component_property="figure" , component_id='polar_plot'),
    Input(component_property='value' , component_id='name_player_1'),
    Input(component_property='value', component_id='name_player_2')
)
def polar_update(player_1, player_2):
    my_variables = ["pace", "passing", "shooting", "physic", "dribbling", "defending"]

    df2 = df.copy()
    df2 = df2[df['short_name'] == player_1]
    df2 = df2.loc[:, my_variables]
    player_1_data = df2.values[0]

    df2 = df.copy()
    df2 = df2[df['short_name'] == player_2]
    df2 = df2.loc[:, my_variables]
    player_2_data = df2.values[0]

    fig = go.Figure(data=
    go.Scatterpolar(
        r=player_1_data,
        theta=my_variables,
        fill='toself',
        marker_color='red'
    )
    )

    fig.add_trace(
        go.Scatterpolar(
            r=player_2_data,
            theta=my_variables,
            fill='toself',
            marker_color='blue'
        )
    )
    return fig

@app.callback(
    Output(component_property="figure" , component_id='perform_player1'),
    Output(component_property="figure" , component_id='perform_player2'),
    Input(component_property='value' , component_id='name_player_1'),
    Input(component_property='value', component_id='name_player_2')
)
def perform(player1, player2):
    val_player_1 = df[df["short_name"]==player1]["potential"].values[0]
    val_player_2 = df[df["short_name"] == player2]["potential"].values[0]
    fig_2 = go.Figure(
        go.Indicator(
            value=val_player_1,
            mode="gauge+number"
        )
    )
    fig_3 = go.Figure(
        go.Indicator(
            value=val_player_2,
            mode="gauge+number",
        )
    )
    return fig_2, fig_3

app.title = "World player performance"

app.run(debug=True)

