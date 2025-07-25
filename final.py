import pandas as pd 
import numpy as np
import plotly.express as px 
import dash
from dash import dcc, html 
from dash.dependencies import Input, Output

# etapa 1, carregar e limpar os dados 
# função para carregar dados com tratamento de exceção
def load_data(file_path):
    try: 
        data= pd.read_csv(file_path, encoding='ISO-8859-1')
        print(f'Dados carregado com sucesso de {file_path}')
        return data
    except:
        print(f'Erro ao carregar os dados de {file_path}')
        return None 
    
# carregar os CSVs
avengers_df = load_data('avengers.csv')
drinks_df = load_data('drinks.csv')

# etapa 2 Limpeza dos dados
# essa função vai limpar os dados, tratando dados nulos e convertendo os seus respectivos tipos
def clean_data(df,numeric_columns):
    try:
        # remover linhas Nulas 
        df = df.dropna()
        #garantir que as colunas numéricas sejam convertidas corretamente.
        for column in numeric_columns:
            df[column] = pd.to_numeric(df[column], errors='coerce')
        print("Dados limpos com sucesso")
        return df 
    except Exception as e:
        print(f'Erro ao limpar os dados: {e}')
        return None    
# limpar avengers
avengers_df = clean_data(avengers_df, ['Appearances'])
#limpar a tabela drinks
drinks_df = clean_data(drinks_df, ['beer_servings', 'spirit_servings', 'wine_servings', 'total_litres_of_pure_alcohol'])
#verificação dos dados após a limpeza
print('\nAvengers DataFrame após a limpeza')
print(avengers_df.head())
print('\nDrinks DataFrame após a limpeza')
print(drinks_df.head())

# Etapa 3 vamos analisar os dados 
def show_statistics(df, title):
    print(f'\nEstatisticas descritivas de {title}')
    print(df.describe())

show_statistics(avengers_df, "Vingadores")
show_statistics(drinks_df,"Consumo de Alcool")

# Etapa 4, criação da visualização com plotly 
def create_avengers_chart():
    return px.bar(
        avengers_df,
        x = 'Name/Alias',
        y = 'Appearances',
        title = 'Numero de aparições dos Vingadores',
        labels ={'Name/Alias':'Personagem', 'Appearances':'Numero de aparições'},
        color = 'Gender'
    )
# função para criar o grafico de consumo de alcool 
def create_drinks_chart():
    return px.bar(
        drinks_df,
        x ='country',
        y = 'total_litres_of_pure_alcohol',
        title = 'Consumo de Alcool por país',
        labels ={'country':'País','total_litres_of_pure_alcohol':'Litros de Alcool' },
        color = 'total_litres_of_pure_alcohol'
    )

app = dash.Dash(__name__) 
app.layout= html.Div([
    html.H1('Analise de dados - Vingadores e Consumo de Alcool', style={'text-align':'center'}),
    #dropdown para escolher a visualização
    dcc.Dropdown(
        id= 'dropdown-chart',
        options=[
            {'label':'Numero de Aparições dos Vingadores', 'value':'avengers'},
            {'label':'Consumo de Alcool por País', 'value':'drinks'}
        ],
        value='avengers',
        style={'width':'50%', 'margin':'auto'}
    ),
    dcc.Graph(id='gragh-output')
])
   
# função de callback para atualizar o grafico baseado na escolha do dropdown
@app.callback(
    Output('graph-output', 'figure'),
    [Input('dropdown-chart', 'value')]
)

def update_graph(chart_type):
    try:
        if chart_type == 'avengers':
            return create_avengers_chart()
        elif chart_type == 'drinks':
            return create_drinks_chart()
    except Exception as e :
        print(f"Erro ao gerar o grafico:{e}")
        return{}

if __name__ =='__main__':
    try:
        app.run(debug=True)
    except Exception as e: 
        print(f'Erro ao rodar o servidor Dash: {e}')