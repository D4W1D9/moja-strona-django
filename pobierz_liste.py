import requests

TMDB_API_KEY = "TWÓJ_KLUCZ_API_TUTAJ" # Wklej swój klucz

def pobierz_top_filmy(ile_stron=25): # Każda strona to 20 filmów (25*20 = 500)
    filmy = []
    print("Pobieram listę najpopularniejszych filmów...")
    
    for strona in range(1, ile_stron + 1):
        url = f"https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}&language=pl-PL&page={strona}"
        response = requests.get(url).json()
        
        for film in response.get('results', []):
            filmy.append(film['title'])
            
    with open("filmy.txt", "w", encoding="utf-8") as f:
        for tytul in filmy:
            f.write(f"{tytul}\n")
            
    print(f"✅ Gotowe! Zapisałem {len(filmy)} filmów do pliku filmy.txt")

if __name__ == "__main__":
    pobierz_top_filmy()