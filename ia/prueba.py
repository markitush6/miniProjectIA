import pandas as pd
import os 
r_cols =  ['anime_id', 'name']

m_cols = ['user_id', 'anime_id', 'rating']

# Ruta base del script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Ruta completa al archivo CSV
anime_path = os.path.join(BASE_DIR, 'datos', 'anime.csv')
ratings_path = os.path.join(BASE_DIR, 'datos', 'rating.csv')

# Cargar los archivos
anime = pd.read_csv(anime_path, sep=',', usecols=range(7), header=0, encoding='ISO-8859-1')
ratings = pd.read_csv(ratings_path, sep=',', usecols=range(3), encoding="ISO-8859-1", low_memory=False)
print(anime.describe())
