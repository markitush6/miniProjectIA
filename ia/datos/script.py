import csv
import requests
import time
import os
from tqdm import tqdm  # Instálalo con: pip install tqdm

INPUT_CSV = os.path.join(os.path.dirname(__file__), 'anime.csv')
OUTPUT_CSV = 'anime_with_images.csv'
API_URL = 'https://api.jikan.moe/v4/anime'

# Tiempo de espera entre peticiones (segundos)
DELAY = 0.5

def fetch_anime_image(anime_name):
    """Busca la URL de la imagen del anime en MyAnimeList usando la API de Jikan."""
    try:
        response = requests.get(API_URL, params={'q': anime_name, 'limit': 1})
        response.raise_for_status()
        data = response.json()
        if data.get('data'):
            anime = data['data'][0]
            images = anime.get('images', {}).get('jpg', {})
            return images.get('large_image_url') or images.get('image_url') or ''
    except Exception:
        return ''
    return ''

def main():
    # Leer los nombres del CSV original
    with open(INPUT_CSV, 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        animes = [row['name'].strip() for row in reader if row.get('name')]

    # Comprobar si ya existe un archivo previo (para reanudar)
    done = {}
    if os.path.exists(OUTPUT_CSV):
        with open(OUTPUT_CSV, 'r', encoding='utf-8') as outfile:
            reader = csv.DictReader(outfile)
            for row in reader:
                done[row['name']] = row['image_url']

    # Abrir el CSV de salida en modo append
    with open(OUTPUT_CSV, 'a', newline='', encoding='utf-8') as outfile:
        fieldnames = ['name', 'image_url']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)

        # Si el archivo está vacío, escribir encabezado
        if os.stat(OUTPUT_CSV).st_size == 0:
            writer.writeheader()

        for name in tqdm(animes, desc="Buscando imágenes"):
            if name in done:
                continue  # ya procesado

            image_url = fetch_anime_image(name)
            writer.writerow({'name': name, 'image_url': image_url})
            outfile.flush()
            time.sleep(DELAY)

if __name__ == '__main__':
    main()
