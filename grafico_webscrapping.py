import dash
from dash import html
import plotly.express as px
import pandas as pd 

#carregar csv
df = pd.read_csv("filmes_adorocinema.csv")
#odernar filmes pelas notas
df.sort_values(by ="Nota", ascending=True)
#criar o grafico com plotly
fig = px.bar(
    df, 
    x="Nota",
    y="Titulo",
    orientation="h",
    labels={"nota": "Nota do Filme", "titulo": "Titulo do filme"},
    title="Nota dos filmes"
)
#inicializando a aplicação dash
app = dash.Dash()

# definindo o layout da aplicação 
app.layout = html.Div([
    html.H1("Grafico de notas dos filmes", style={'text-align': 'center'}),
    html.Div([
        html.Iframe(
            srcDoc=fig.to_html(),
            width="100%",
            height= "600px",
            style={"border": "none"}
        )
    ], style={'padding':'15px'})
])
#rodar a aplicação
if __name__ =='__main__':
    app.run(debug=True)

