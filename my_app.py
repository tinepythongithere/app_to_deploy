from dash import Dash, html, dcc
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import pandas as pd
from dash.dependencies import Input, Output

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

app = Dash(external_stylesheets=[dbc.themes.MATERIA])

app.layout = html.Div([
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