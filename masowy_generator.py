import os
import django
import requests
from django.core.files.base import ContentFile
import time

# 1. Konfiguracja Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mywebsite.settings')
django.setup()

from movies.models import Movie

# --- KONFIGURACJA ---
TMDB_API_KEY = "66dee6fbbff465c8ef3607dbfb4a37ea"
FILENAME = "filmy.txt"

def importuj_z_pliku():
    if not os.path.exists(FILENAME):
        print(f"❌ BŁĄD: Nie widzę pliku {FILENAME}! Stwórz go w folderze projektu.")
        return

    # Czytamy tytuły z pliku
    with open(FILENAME, 'r', encoding='utf-8') as f:
        lista_filmow = [line.strip() for line in f if line.strip()]

    print(f"🚀 Rozpoczynam wielki import: {len(lista_filmow)} filmów do przetworzenia.")
    
    sukcesy = 0
    pominiecia = 0

    for index, tytul in enumerate(lista_filmow, 1):
        # Sprawdzamy, czy film już jest w bazie (żeby nie dublować przy restartach)
        if Movie.objects.filter(title__iexact=tytul).exists():
            print(f"[{index}/{len(lista_filmow)}] ⏭️ {tytul} już jest w bazie, pomijam.")
            pominiecia += 1
            continue

        print(f"[{index}/{len(lista_filmow)}] 🔍 Szukam i dodaję: {tytul}...")
        
        search_url = "https://api.themoviedb.org/3/search/movie"
        params = {'api_key': TMDB_API_KEY, 'query': tytul, 'language': 'pl-PL'}
        
        try:
            res = requests.get(search_url, params=params).json()
            if res.get('results'):
                dane = res['results'][0]
                full_title = dane.get('title')
                year_raw = dane.get('release_date', '0000')[:4]
                year = int(year_raw) if year_raw.isdigit() else 2000
                poster_path = dane.get('poster_path')

                # Tworzymy rekord w bazie
                nowy_film = Movie.objects.create(title=full_title, year=year)

                if poster_path:
                    img_url = f"https://image.tmdb.org/t/p/w600_and_h900_bestv2{poster_path}"
                    img_res = requests.get(img_url)
                    if img_res.status_code == 200:
                        nowy_film.cover.save(f"poster_{nowy_film.id}.jpg", ContentFile(img_res.content), save=True)
                
                print(f"  ✅ Sukces: {full_title} ({year})")
                sukcesy += 1
            else:
                print(f"  ❌ Nie znaleziono filmu '{tytul}' w TMDB.")

        except Exception as e:
            print(f"  ❌ Błąd przy '{tytul}': {e}")
        
        # Mały odstęp, żeby TMDB nas nie zbanowało (0.1s przy 400 filmach to tylko 40 sekund czekania)
        time.sleep(0.1)

    print(f"\n🎉 MISJA ZAKOŃCZONA!")
    print(f"Dodano nowych: {sukcesy}")
    print(f"Pominięto (już były): {pominiecia}")

if __name__ == '__main__':
    importuj_z_pliku()