import pandas as pd
import pickle
import os

CORR_PATH = 'ia/corrMatrix.pkl'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Siempre cargamos los datos base
anime_path = os.path.join(BASE_DIR, 'datos', 'anime.csv')
ratings_path = os.path.join(BASE_DIR, 'datos', 'rating.csv')

r_cols =  ['anime_id', 'name']
animes= pd.read_csv(anime_path, sep=',', usecols=range(7), header=0, encoding='ISO-8859-1')

m_cols = ['user_id', 'anime_id', 'rating']
ratings = pd.read_csv(ratings_path, sep=',', usecols=range(3), encoding="ISO-8859-1", low_memory=False)
print(animes.describe())

# Limpiar ratings
ratings['rating'] = pd.to_numeric(ratings['rating'], errors='coerce')
ratings = ratings.dropna(subset=['rating'])
ratings = ratings[ratings['rating'] != -1]

# Filtrar animes con suficientes valoraciones
counts = ratings['anime_id'].value_counts()
users = ratings['user_id'].value_counts()

min_ratings = 100
animes_to_keep = counts[counts >= min_ratings].index
filterRatings = ratings[ratings['anime_id'].isin(animes_to_keep)]

# Filtrar usuarios con actividad razonable
min_user_ratings = 50
max_user_ratings = 300
ratingsFilter = users[(users >= min_user_ratings) & (users <= max_user_ratings)]
filterRatings = filterRatings[filterRatings['user_id'].isin(ratingsFilter.index)]

# Crear matriz usuario-anime
userRatings = filterRatings.pivot_table(index='user_id', columns='anime_id', values='rating')

# Cargar o calcular correlación
if os.path.exists(CORR_PATH):
    with open(CORR_PATH, 'rb') as f:
        corrMatrix = pickle.load(f)
    print("✅ Matriz de correlación cargada.")
else:
    corrMatrix = userRatings.corr(method='pearson', min_periods=500)
    with open(CORR_PATH, 'wb') as f:
        pickle.dump(corrMatrix, f)
    print("✅ Matriz de correlación calculada y guardada.")

# Añadir valoraciones del usuario
myRatings = pd.Series({11061: 10, 2476: 1}, name=0)
userRatings = pd.concat([userRatings, myRatings.to_frame().T])

# Renombrar columnas con nombres de animes
name_map = animes.set_index('anime_id')['name'].to_dict()
userRatings = userRatings.rename(columns=name_map)
corrMatrix_names = corrMatrix.rename(index=name_map, columns=name_map)

# Extraer valoraciones del usuario
myRatings = userRatings.loc[0].dropna()

# Generar recomendaciones
simCandidates = pd.Series(dtype='float64')

for anime, rating in myRatings.items():
    if anime in corrMatrix_names:
        sims = corrMatrix_names[anime].dropna()
        sims = sims * rating
        simCandidates = pd.concat([simCandidates, sims])

simCandidates = simCandidates.groupby(simCandidates.index).sum()
filteredSims = simCandidates.drop(myRatings.index, errors='ignore')
filteredSims = filteredSims.sort_values(ascending=False)

# Mostrar resultados
print("🎯 Recomendaciones:")
print(filteredSims.head(10))