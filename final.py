import pandas as pd
import numpy as np
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import os

# Etapa 1: carregar e limpar os dados
def load_data(file_path):
    try:
        data = pd.read_csv(file_path, encoding='utf-8')
        print(f'Dados carregados com sucesso de {file_path} (UTF-8)')
        return data
    except UnicodeDecodeError:
        try:
            data = pd.read_csv(file_path, encoding='ISO-8859-1')
            print(f'Dados carregados com sucesso de {file_path} (ISO-8859-1)')
            return data
        except Exception as e:
            print(f'Erro ao carregar os dados de {file_path}: {e}')
            return None
    except Exception as e:
        print(f'Erro inesperado ao carregar os dados de {file_path}: {e}')
        return None

# Carregar os CSVs
script_dir = os.path.dirname(os.path.abspath(__file__))
avengers_df = load_data(os.path.join(script_dir, 'avengers.csv'))
drinks_df = load_data(os.path.join(script_dir, 'drinks.csv'))

# Etapa 2: Limpeza dos dados
def clean_data(df, numeric_columns):
    try:
        # Remover apenas linhas com dados faltando nas colunas críticas
        df = df.dropna(subset=numeric_columns)

        for column in numeric_columns:
            if column in df.columns:
                df[column] = pd.to_numeric(df[column], errors='coerce')
            else:
                print(f"Aviso: coluna '{column}' não encontrada no DataFrame.")

        df = df.dropna(subset=numeric_columns)  # Segunda limpeza após conversão
        print('Dados limpos com sucesso')
        return df
    except Exception as e:
        print(f'Erro ao limpar os dados: {e}')
        return None

# Limpar avengers
avengers_df = clean_data(avengers_df, ['Appearances']) if avengers_df is not None else None

# Limpar drinks
drinks_df = clean_data(drinks_df, ['beer_servings', 'spirit_servings', 'wine_servings', 'total_litres_of_pure_alcohol']) if drinks_df is not None else None

# Verificação dos dados após a limpeza
print('\nAvengers Dataframe após a limpeza')
print(avengers_df.head() if avengers_df is not None else 'Erro: Avengers DataFrame não disponível')

print('\nDrinks Dataframe após a limpeza')
print(drinks_df.head() if drinks_df is not None else 'Erro: Drinks DataFrame não disponível')

# Etapa 3: Estatísticas
def show_statistics(df, title):
    if df is not None:
        print(f'\nEstatísticas descritivas de {title}')
        print(df.describe())
    else:
        print(f'Dados indisponíveis para: {title}')

show_statistics(avengers_df, "Vingadores")
show_statistics(drinks_df, "Consumo de Álcool")

# Etapa 4: Visualizações com Plotly
def create_avengers_chart():
    if avengers_df is not None and not avengers_df.empty:
        return px.bar(
            avengers_df,
            x='Name/Alias',
            y='Appearances',
            title='Número de aparições dos Vingadores',
            labels={'Name/Alias': 'Personagem', 'Appearances': 'Número de aparições'},
            color='Gender'
        )
    else:
        return px.scatter(title="Dados de Vingadores indisponíveis")

def create_drinks_chart():
    if drinks_df is not None and not drinks_df.empty:
        return px.bar(
            drinks_df,
            x='country',
            y='total_litres_of_pure_alcohol',
            title='Consumo de Álcool por País',
            labels={'country': 'País', 'total_litres_of_pure_alcool': 'Litros de Álcool'},
            color='total_litres_of_pure_alcohol'
        )
    else:
        return px.scatter(title="Dados de Consumo de Álcool indisponíveis")

# Etapa 5: App Dash
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1('Análise de Dados - Vingadores e Consumo de Álcool', style={'text-align': 'center'}),
    dcc.Dropdown(
        id='dropdown-chart',
        options=[
            {'label': 'Número de Aparições dos Vingadores', 'value': 'avengers'},
            {'label': 'Consumo de Álcool por País', 'value': 'drinks'}
        ],
        value='avengers',
        style={'width': '50%', 'margin': 'auto'}
    ),
    dcc.Graph(id='graph-output')
])

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
        else:
            return px.scatter(title="Tipo de gráfico desconhecido")
    except Exception as e:
        print(f"Erro ao gerar o gráfico: {e}")
        return px.scatter(title="Erro ao gerar gráfico")

# Run server
if __name__ == '__main__':
    try:
        app.run(debug=True)
    except Exception as e:
        print(f'Erro ao rodar o servidor Dash: {e}')