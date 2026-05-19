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

    dbc.Row([
    dbc.Col(
        html.Div(id="graf")
    )
])
])

@callback(
    Output(component_id='graf', component_property='children'),
    Input(component_id='dropdown-art', component_property='value'),
)
def update_graphs(input):

    if input is None or input == []:
        return []

    grafs = []

    for i in input:

        c = "".join(
            df[df["corpus_id"] == i]["c_word"].tolist()
        )

        di = {k: Counter(c)[k]
    for k in ['u', 'p', 'P', 'a', 'A', 's', 'S']
}


        fig = px.bar(
            x=list(di.keys()),
            y=list(di.values()),
            labels={
                "x": "Letras",
                "y": "Ocorrências"
            },
            title=i
        )
        fig.update_layout(title_x=0.5)
        
        fig.update_traces(
    hovertemplate=
    f"Letra: %{{x}}<br>" +
    f"Ocorrências: %{{y}}<br>" +
    f"Artista: {i}<br>" +
    "<extra></extra>"
)

        grafs.append(
            dbc.Col(
                dcc.Graph(figure=fig),
                width=4
            )
        )

    return dbc.Row(grafs)        

if __name__ == '__main__':
    app.run(debug=True)