from dash import Dash, html, dcc
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import pandas as pd
from dash.dependencies import Input, Output
import dash_daq as daq

df = pd.read_csv("data/players_21.csv")
#============================================================
names = df.loc[:,'short_name']

#============================================================
name_players_1 = dcc.Dropdown(
    options=[
        {'label': i, 'value': i} for i in names
    ],
    #multi=True,
    value=names[0],
    id= 'name_player_1',
    #style={'width':'65%'}
)

name_players_2 = dcc.Dropdown(
    options=[
        {'label': i, 'value': i} for i in names
    ],
    #multi=True,
    value=names[1],
    id= 'name_player_2',
    #style={'width':'65%'}
)

name = dcc.Dropdown(
    options=[
        {'label': i, 'value': i} for i in names
    ],
    #multi=True,
    value=names[0],
    id= 'name',
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
                html.Label("Short Name ...", id='sname'),
                html.Label("Nationalité", id='nationalite'),
                html.Label("Pieds Fort", id='pieds_fort')
            ], style={'display':'flex','align-items':'center'})
        ], width={'size':3, 'offset':1}),
        dbc.Col([
            dbc.Card([
                html.Label("Long name", id='long_name'),
                html.Hr(),
                html.Label("Club actuel", id='club_actuel'),
                html.Hr(),
                html.Label("Poids" , id='poids'),
                html.Hr(),
                html.Label("Taille", id='taille'),
                html.Hr(),
                html.Label("Valeur (en £)", id='valeur')
            ], style={'padding':'15px'})
        ], width=6),
    ]),
    html.Label(""),
    dbc.Row([
        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    html.Label('Player'),
                    name
                ], style={'text-align': 'center'})
            )], width={'size':3, 'offset':1}),

        dbc.Col([
            dbc.Card([
                daq.Slider(
                    min=0,
                    max=100,
                    value=30,
                    id='potentiel',
                    disabled=True,
                    handleLabel={"showCurrentValue": True,"label": "Potential"},
                ),
                html.Br(),html.Br(),
                daq.Slider(
                    min=0,
                    max=5,
                    value=3,
                    id='reputation',
                    disabled=True,
                    handleLabel={"showCurrentValue": True,"label": "Reputation"},
                ),
                html.Br(),html.Br(),
                daq.Slider(
                    min=0,
                    max=100,
                    value=30,
                    id='pace',
                    disabled=True,
                    handleLabel={"showCurrentValue": True,"label": "Pace"},
                ),
                html.Br(),html.Br(),
                daq.Slider(
                    min=0,
                    max=100,
                    value=20,
                    id='shooting',
                    disabled=True,
                    handleLabel={"showCurrentValue": True,"label": "Shooting"},
                ),
                html.Br(),html.Br(),
                daq.Slider(
                    min=0,
                    max=100,
                    value=70,
                    id='dribbling',
                    disabled=True,
                    handleLabel={"showCurrentValue": True,"label": "Dribbling"},
                ),
                html.Br(),html.Br(),
                daq.Slider(
                    min=0,
                    max=100,
                    value=38,
                    id='physic',
                    disabled=True,
                    handleLabel={"showCurrentValue": True,"label": "Physic"}),
                html.Br(),html.Br(),
                daq.Slider(
                    min=0,
                    max=100,
                    value=58,
                    id='defending',
                    color='red',
                    disabled=True,
                    handleLabel={"showCurrentValue": True,"label": "Defending"},
                ),
            ], style={'padding':'15px'})
        ], width={'size':4, 'offset':0}),
    ])

])

content = html.Div(id="page-content")

app.layout = html.Div([
    dcc.Location(id="url", pathname="/fiche_perso"),
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

@app.callback(
    Output(component_property="children", component_id='sname'),
    Output(component_property="children", component_id='nationalite'),
    Output(component_property="children", component_id='pieds_fort'),
    Input(component_property='value', component_id='name'),
)
def infos(player):

    short_name = df[df["short_name"]==player]["short_name"].values[0]
    nationalite = df[df["short_name"]==player]["nationality"].values[0]
    pieds_fort = df[df["short_name"]==player]["preferred_foot"].values[0]
    return short_name, "Nationalité : "+nationalite, "Pieds fort : "+pieds_fort


@app.callback(
    Output(component_property="children", component_id='long_name'),
    Output(component_property="children", component_id='club_actuel'),
    Output(component_property="children", component_id='poids'),
    Output(component_property="children", component_id='taille'),
    Output(component_property="children", component_id='valeur'),
    Input(component_property='value', component_id='name'),
)
def infos(player):

    long_name = df[df["short_name"]==player]["long_name"].values[0]
    club_name = df[df["short_name"]==player]["club_name"].values[0]
    poids = df[df["short_name"]==player]["weight_kg"].values[0]
    taille = df[df["short_name"] == player]["height_cm"].values[0]
    valeur = df[df["short_name"] == player]["value_eur"].values[0]
    return "Long name : "+long_name, "Club actuel : "+club_name, "Poids : "+str(poids), \
        "Taille (en cm) : "+str(taille), "Valeur (en £) : "+str(valeur)


@app.callback(
    Output(component_property="value", component_id='potentiel'),
    Output(component_property="value", component_id='reputation'),
    Output(component_property="value", component_id='pace'),
    Output(component_property="value", component_id='shooting'),
    Output(component_property="value", component_id='dribbling'),
    Output(component_property="value", component_id='physic'),
    Output(component_property="value", component_id='defending'),
    Input(component_property='value', component_id='name'),
)
def stats(player):
    potentiel = df[df["short_name"] == player]["potential"].values[0]
    reputation = df[df["short_name"] == player]["international_reputation"].values[0]
    pace = df[df["short_name"] == player]["pace"].values[0]
    shooting = df[df["short_name"] == player]["shooting"].values[0]
    dribbling = df[df["short_name"] == player]["dribbling"].values[0]
    physic = df[df["short_name"] == player]["physic"].values[0]
    defending = df[df["short_name"] == player]["defending"].values[0]
    return potentiel, reputation, pace, shooting,dribbling, physic, defending



app.title = "World player performance"

app.run(debug=True)

