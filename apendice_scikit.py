# importa o algoritmo de clustering do kmeans da biblioteca scikit-learn
from sklearn.cluster import KMeans 
# importa o escalador StandardScaler para padronizar os dados
from sklearn.preprocessing import StandardScaler

# definir os dados de exemplo
# sera uma lista de listas
x = [[1,2], [1,4], [1,0], [10,2], [10,4], [10,0]]

# vamos instanciar o standard para padronizar os dados 
scaler = StandardScaler()

# aplicar o escalador nos dados para que tenham média 0 e desvio padrão 1
X_scaled =scaler.fit_transform(x)

# cria a instacia do algoritmo KMeans com 2 clusters
kmeans= KMeans(n_clusters=2, random_state=42)

# aplicar o algoritmo do kmeans aos dados padronizados
kmeans.fit(X_scaled)

# exibir os rotulos(clusters) atribuidos a cada ponto 
print(kmeans.labels_)

