from dash import Dash, State, html, dcc, callback, Output, Input
import dash_ag_grid as dag
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from collections import Counter
from plotly.graph_objects import Figure

df=pd.read_csv('https://raw.githubusercontent.com/ProjetoMPB/mpb-corpus/refs/heads/main/dataset/contour_rhythm.csv',keep_default_na=False)
artistas = sorted(list(set(df["corpus_id"].tolist())))

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
            meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"},
    ])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Dashboard projeto MPB",
                        className="text-center fs-1, mb-4"), width=12)
    ]),

    dbc.Row([
        dbc.Col(html.H5("Selecione o parâmetro",  className="text-center fs-1, mb-4"),
                          width={"size": 12, "offset": 0, "order": 1})
    ]),
    
     dbc.Row([
        dbc.Col(dcc.Dropdown(id="dropdown-par", options=['c-letras', 'r-letras'], className="mb-4"),
            width={"size": 4, "offset": 4, "order": 1})
            ]),


    dbc.Row([
        dbc.Col(html.H5("Selecione os artistas",  className="text-center fs-1, mb-4"),
                          width={"size": 12, "offset": 0, "order": 1})
    ]),

    dbc.Row([
        dbc.Col(dcc.Dropdown(id="dropdown-art", multi= True,  options=artistas, labels={
            'select_all': 'selecionar todos',
            'deselect_all': 'limpar a seleção'}),
            width={"size": 12, "offset": 0, "order": 1})
            ]),
#aqui entram os gráficos
    dbc.Row([
    dbc.Col(
        html.Div(id="graf")
    )
])
])
@callback(
    Output(component_id='graf', component_property='children'),
    Input(component_id="dropdown-par",component_property="value"),
    Input(component_id='dropdown-art', component_property='value'),
)
def gera_graficos(input_par, input_art):
#deixa zerado antes de qualquer input
    if input_par is None:
        return []
    if input_art is None or input_art == []:
        return []
    if input_par == "c-letras":
#cria lista vazia para graficos
        grafs = []
#itera para cada grafico
        for i in input_art:
#junta todas as palavras usadas pelo artista
            c = "".join(
                df[df["corpus_id"] == i]["c_word"].tolist()
                )
#conta o numero de apariçoes de cada letra e gera um dicionario
            di = {k: Counter(c)[k]
            for k in ['u', 'p', 'P', 'a', 'A', 's', 'S']
            }
#calcula porcentagem de uso
            porcentagem = [
        (v / sum(di.values())) *100 
        for v in di.values()
        ]
#gera os graficos
            fig = px.bar(
                x=list(di.keys()),
                y=list(porcentagem),
                labels={
                    "x": "Letras",
                    "y": "Porcentagem de uso"
                },
                title=i
            )
#centraliza o titulo
            fig.update_layout(title_x=0.5)
#da nome pra cada letra
            labels = {
        'u': 'Uníssono',
        'p': 'Passo descendente',
        'P': 'Passo ascendente',
        'a': 'Arpejo descendente',
        'A': 'Arpejo ascendente',
        's': 'Salto descendente',
        'S': 'Salto ascendente'
    }
    #gera uma lista com os novos nomes e com os valores de aparição
            customdata = [
        [
            labels[k],
            v
        ]
        for k, v in di.items()
    ]
    #define o hover
            fig.update_traces(
                customdata=customdata,
        hovertemplate=
        "C-letra: %{x}<br>" +
        "Descrição da C-letra: %{customdata[0]}<br>" +
        "Percentual de uso: %{y:.2f}%<br>"
        "Número de usos da letra: %{customdata[1]}<br>"
        f"Artista: {i}<br>" +
        "<extra></extra>"
    )
    #adiciona cada grafico em uma coluna 
            grafs.append(
                dbc.Col(
                    dcc.Graph(figure=fig),
                    width=4

                )
            )
    # caso a row encha ele automaticamente cria uma nova
        return dbc.Row(grafs)   
    if input_par == "r-letras":
#cria lista vazia para graficos
        grafs = []
#itera para cada grafico
        for i in input_art:
#junta todas as palavras usadas pelo artista
            c = "".join(
                df[df["corpus_id"] == i]["r_word"].tolist()
                )
#conta o numero de apariçoes de cada letra e gera um dicionario
            di = {k: Counter(c)[k]
            for k in ['a', 'b', 'c', 'd', 'e', 'f', 'g','h', 'i', 'j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
            }
#calcula porcentagem de uso
            porcentagem = [
        (v / sum(di.values())) *100 
        for v in di.values()
        ]
#gera os graficos
            fig = px.bar(
                x=list(di.keys()),
                y=list(porcentagem),
                labels={
                    "x": "Letras",
                    "y": "Porcentagem de uso"
                },
                title=i
            )
#centraliza o titulo
            fig.update_layout(title_x=0.5)
#da nome pra cada letra
            labels = {
        'a': '□□□□ □□□□ □□□□',
        'b': '■□□□ □□□□ □□□□',
        'c': '□□□■ □□□□ □□□□',
        'd': '□□□□ ■□□□ □□□□',
        'e': '□□□□ □□■□ □□□□',
        'f': '□□□□ □□□□ ■□□□',
        'g': '□□□□ □□□□ □■□□',
        'h': '■□□■ □□□□ □□□□',
        'i': '■□□□ ■□□□ □□□□',
        'j': '■□□□ □□■□ □□□□',
        'k': '■□□□ □□□□ ■□□□',
        'l': '■□□□ □□□□ □■□□',
        'm': '□□□■ □□■□ □□□□',
        'n': '□□□■ □□□□ □■□□',
        'o': '□□□□ ■□□□ ■□□□',
        'p': '□□□□ □□■□ □■□□',
        'q': '■□□■ □□■□ □□□□',
        'r': '■□□■ □□□□ □■□□',
        's': '■□□□ ■□□□ ■□□□',
        't': '■□□□ □□■□ □■□□',
        'u': '□□□■ □□■□ □■□□',
        'v': '■□□■ □□■□ □■□□',
        'w': '■□□□ □□■□ ■□■□',
        'x': '■□□■ □□■□ ■□■□',
        'y': '□□■□ ■□■□ ■□■□',
        'z': '■□■□ ■□■□ ■□■□'
    }
    #gera uma lista com os novos nomes e com os valores de aparição
            customdata = [
        [
            labels[k],
            v
        ]
        for k, v in di.items()
    ]
    #define o hover
            fig.update_traces(
                customdata=customdata,
        hovertemplate=
        "R-letra: %{x}<br>" +
        "Pontos de ataque: %{customdata[0]}<br>" +
        "Percentual de uso: %{y:.2f}%<br>"
        "Número de usos da letra: %{customdata[1]}<br>"
        f"Artista: {i}<br>" +
        "<extra></extra>"
    )
    #adiciona cada grafico em uma coluna 
            grafs.append(
                dbc.Col(
                    dcc.Graph(figure=fig),
                    width=12

                )
            )
    # caso a row encha ele automaticamente cria uma nova
        return dbc.Row(grafs)     

if __name__ == '__main__':
    app.run(debug=True)
