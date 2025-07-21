# 03_grafico.py
import dash 
from dash import dcc, html 
from dash.dependencies import Input, Output 
import plotly.graph_objs as go
# Dicionarios com as Informações da caixa de Dropdown
dados_conceitos = {
    "java":{'Variaveis':8, 'Condicionais':10, 'Loops':4, 'Poo':3, 'Funções':4}, 
    "python":{'Variaveis':9, 'Condicionais':7, 'Loops':8, 'Poo':7, 'Funções':2}, 
    "sql":{'Variaveis':10, 'Condicionais':9, 'Loops':1, 'Poo':6, 'Funções':8}, 
    "golang":{'Variaveis':7, 'Condicionais':5, 'Loops':3, 'Poo':5, 'Funções':3}, 
    "javascript":{'Variaveis':6, 'Condicionais':2, 'Loops':4, 'Poo':4, 'Funções':6}
}
cores_map = dict(
    Java = "red",
    Python = "green",
    SQl = "yellow",
    Golang = "blue",
    Javascrip = "pink"
)
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H4('Cursos de TI', style={'textAlign': 'center'}), 
    html.Div(
        dcc.Dropdown(
           id = "dropdown_linguagens", 
           options = [
               {'label': 'Java', 'value': 'java'},
               {'label': 'Python', 'value': 'python'},
               {'label': 'SQL', 'value': 'sql'},
               {'label': 'GoLand', 'value': 'goland'},
               {'label': 'JavaScript', 'value': 'javascript'}
           ],
           value = ["java"], 
           multi = True,
           style = {'width':'50%', 'margin':'0 auto'}
        )
    ),
    dcc.Graph(id='grafico_linguagem')   
], style = {'width':'80%', 'margin':'0 auto'}
)
# Uma função que vai ser chamada atravez do evento
@app.callback(
    Output('grafico_linguagem', 'figure'),
    [input('dropdown_linguages','valeu')]
)
def scarter_linguagens(linguagens_selecionadas):
    scarter_trace = []
    for linguagem in linguagens_selecionadas:
        dados_linguagem = dados_conceitos[linguagem]
        for conceito, conhecimento in dados_linguagem.items():
            scarter_trace.append(
                go.Scatter(
                    x = [conceito],
                    y = [conhecimento],
                    mode = 'markers', 
                    name = linguagem.title(),
                    marker = {'size':15, 'color': cores_map[linguagem]},
                    showlegend=False
                )
            )
    scarter_layout = go.Layout(
        title= 'Meus conhecimentos em Linguagens',
        xaxis= dict(title ='conceito', showgrid=False),
        yaxis=dict(title = 'Niveis de Conhecimento',  showgrid=False)
    )
    return {'data': scarter_trace, 'layout': scarter_layout}
if __name__ == "__main__":
    app.run(debug=True)
