import requests
import csv
import time
import os
from tqdm import tqdm

OUTPUT_CSV = 'anime_with_images.csv'
API_URL = 'https://api.jikan.moe/v4/anime'
DELAY = 0.5

def fetch_anime_image(anime_name):
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

def procesar_recomendaciones(recomendaciones):
    # Limitar a solo 10 recomendaciones
    recomendaciones = recomendaciones[:10]

    # Crear diccionario con resultados
    resultados = {}

    for name in tqdm(recomendaciones, desc="Buscando imágenes"):
        image_url = fetch_anime_image(name)
        resultados[name] = image_url
        time.sleep(DELAY)

    # Escribir el archivo desde cero
    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as outfile:
        fieldnames = ['name', 'image_url']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for name, image_url in resultados.items():
            writer.writerow({'name': name, 'image_url': image_url})

# # Ejemplo de uso
# if __name__ == '__main__':
#     recomendaciones = [
#         "Naruto", "One Piece", "Attack on Titan", "Death Note", "Fullmetal Alchemist",
#         "Demon Slayer", "Jujutsu Kaisen", "My Hero Academia", "Tokyo Ghoul", "Bleach"
#     ]
#     procesar_recomendaciones(recomendaciones)