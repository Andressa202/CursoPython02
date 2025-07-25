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
            df[column] = pd.to_numeric(df[column], erros='coerce')
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
print('\nAvengers DataFrame após limpeza')
print(avengers_df.head())
print('\nDrinks DataFRame após limpeza')
print(drinks_df.head())
        