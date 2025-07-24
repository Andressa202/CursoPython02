from sklearn.cluster import KMeans  # Importa o algoritmo de agrupamento KMeans
from sklearn.preprocessing import StandardScaler  # Importa o normalizador de dados para padronização

@app.route('/insights_3d')
def insights_3d():
    # Abrimos o banco de dados SQLite para leitura das tabelas salvas
    with sqlite3.connect(DB_PATH) as conn:
        inad_df = pd.read_sql_query("SELECT * FROM inadimplencia", conn)  # Lê os dados de inadimplência
        selic_df = pd.read_sql_query("SELECT * FROM selic", conn)  # Lê os dados da taxa SELIC

    # Mescla os dois dataframes com base na coluna 'mes', ordenando do mais antigo para o mais recente
    merged = pd.merge(inad_df, selic_df, on='mes').sort_values('mes')
    merged['mes_idx'] = range(len(merged))  # Cria um índice numérico sequencial para representar o tempo no gráfico

    # Calcula a diferença de inadimplência em relação ao mês anterior (primeira derivada discreta)
    merged['tend_inad'] = merged['inadimplencia'].diff().fillna(0)
    # Classifica a tendência como "subiu", "caiu" ou "estável" com base na variação calculada
    trend_color = ['subiu' if x > 0 else 'caiu' if x < 0 else 'estável' for x in merged['tend_inad']]

    # Calcula as variações mensais (derivadas discretas) da inadimplência e da SELIC
    merged['var_inad'] = merged['inadimplencia'].diff().fillna(0)
    merged['var_selic'] = merged['selic_diaria'].diff().fillna(0)

    # Seleciona apenas as colunas numéricas que serão usadas para agrupar os meses por similaridade
    features = merged[['selic_diaria', 'inadimplencia']].copy()
    scaler = StandardScaler()  # Inicializa o normalizador para padronizar as variáveis (média=0, desvio=1)
    scaled_features = scaler.fit_transform(features)  # Aplica a normalização nas colunas selecionadas

    # Executa o algoritmo KMeans com 3 clusters (grupos) distintos
    # Isso vai rotular cada mês com um número de cluster, agrupando meses similares
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    merged['cluster'] = kmeans.fit_predict(scaled_features)  # Adiciona a coluna com os clusters atribuídos

    # Prepara os dados de entrada para o cálculo de uma regressão linear múltipla
    # A ideia é encontrar um plano z = a*x + b*y + c que melhor se ajusta aos pontos 3D
    X = merged[['mes_idx', 'selic_diaria']].values  # Matriz de entrada: tempo (mes_idx) e selic
    Y = merged['inadimplencia'].values  # Vetor de saída: inadimplência

    # np.c_ concatena uma coluna de 1s para permitir o cálculo do termo independente 'c' (intercepto)
    A = np.c_[X, np.ones(X.shape[0])]
    # Aplica o método dos mínimos quadrados para resolver A * coef = Y
    # Resultado: coef[0] = a, coef[1] = b, coef[2] = c (parâmetros do plano)
    coeffs, _, _, _ = np.linalg.lstsq(A, Y, rcond=None)

    # Criamos uma malha (grid) de pontos em 2D para desenhar a superfície do plano de regressão
    xi = np.linspace(merged['mes_idx'].min(), merged['mes_idx'].max(), 30)  # 30 pontos entre o menor e o maior mês
    yi = np.linspace(merged['selic_diaria'].min(), merged['selic_diaria'].max(), 30)  # 30 pontos entre min e max da SELIC
    xi, yi = np.meshgrid(xi, yi)  # Gera todas as combinações possíveis entre os valores de xi e yi (grade 2D)
    zi = coeffs[0]*xi + coeffs[1]*yi + coeffs[2]  # Aplica a equação do plano para gerar os valores z (inadimplência)

    # Cria o gráfico de pontos 3D com informações extras no hover
    scatter = go.Scatter3d(
        x=merged['mes_idx'],  # eixo x = tempo
        y=merged['selic_diaria'],  # eixo y = taxa SELIC
        z=merged['inadimplencia'],  # eixo z = inadimplência
        mode='markers',  # apenas marcadores (bolinhas)
        marker=dict(
            size=8,
            color=merged['cluster'],  # define a cor com base no cluster de cada ponto
            colorscale='Viridis',  # paleta de cores suave
            opacity=0.9  # transparência
        ),
        text=[  # conteúdo que aparece ao passar o mouse sobre os pontos
            f"Mês: {m}<br>Inadimplência: {z:.2f}%<br>SELIC: {y:.2f}%<br>Var Inad: {vi:.2f}<br>Var SELIC: {vs:.2f}<br>Tendência: {t}"
            for m, z, y, vi, vs, t in zip(
                merged['mes'], merged['inadimplencia'], merged['selic_diaria'],
                merged['var_inad'], merged['var_selic'], trend_color
            )
        ],
        hovertemplate='%{text}<extra></extra>'  # Exibe apenas o texto personalizado
    )

    # Cria a superfície 3D do plano de regressão
    surface = go.Surface(
        x=xi, y=yi, z=zi,  # coordenadas da grade
        showscale=False,  # não mostrar barra de cores
        colorscale='Reds',  # paleta vermelha para o plano
        opacity=0.5,  # plano parcialmente transparente
        name='Plano de Regressão'  # legenda
    )

    # Junta os dois gráficos (pontos e plano) em uma única visualização 3D
    fig = go.Figure(data=[scatter, surface])

    # Define o layout da cena 3D
    fig.update_layout(
        scene=dict(
            xaxis=dict(title='Tempo (Meses)', tickvals=merged['mes_idx'], ticktext=merged['mes']),
            yaxis=dict(title='SELIC (%)'),
            zaxis=dict(title='Inadimplência (%)')
        ),
        title='Insights Econômicos 3D com Tendência, Derivadas e Clusters',
        margin=dict(l=0, r=0, t=50, b=0),
        height=800
    )

    # Converte o gráfico Plotly para HTML (sem a estrutura HTML completa)
    graph_html = fig.to_html(full_html=False, include_plotlyjs='cdn')

    # Renderiza uma página HTML simples com o gráfico incluído no centro
    return render_template_string('''
        <html>
        <head>
            <title>Insights Econômicos 3D</title>
            <style>
                body { font-family: Arial, sans-serif; background-color: #f8f9fa; color: #222; text-align: center; }
                .container { width: 95%; margin: auto; }
                a { text-decoration: none; color: #007bff; }
                a:hover { text-decoration: underline; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Gráfico 3D com Insights Econômicos</h1>
                <p>Análise visual com clusters, tendências e plano de regressão.</p>
                <div>{{ grafico|safe }}</div>
                <br><a href="/">Voltar</a>
            </div>
        </body>
        </html>
    ''', grafico=graph_html)
