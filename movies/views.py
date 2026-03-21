import requests
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Movie, GlobalMovie
from .forms import MovieForm
from django.core.files.base import ContentFile
import os

# --- KONFIGURACJA AI ---
# Wklej poniżej swój prawdziwy klucz API z OpenAI.
# Znajdziesz go na stronie: https://platform.openai.com/api-keys
OPENAI_API_KEY = "WSTAW_TUTAJ_SWÓJ_KLUCZ_OPENAI_API"
# ---------------------

def generate_ai_poster(title, director, year):
    """
    Tworzy minimalistyczny plakat filmowy przy użyciu DALL-E 3 na podstawie metadanych.
    """
    if OPENAI_API_KEY == "WSTAW_TUTAJ_SWÓJ_KLUCZ_OPENAI_API":
        print("BŁĄD: Nie wstawiłeś klucza API do OpenAI w views.py!")
        return None, None

    try:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)

        # Tworzymy zaawansowany prompt dla AI, używając tytułu, reżysera i roku.
        # Im lepszy opis, tym lepszy plakat.
        prompt = (
            f"A professional, minimalist, and artistic movie poster for the film '{title}' "
            f"directed by '{director}', released in the year {year}. The style should be high-quality, "
            f"modern graphic design, without photographic realism. It should emphasize key themes. "
            f"The title '{title}' must be prominent, clear, and stylized. Dark and cool color palette. "
            f"Minimalistic elements. No clutter. Text is stylized."
        )

        print(f"Rozpoczynam generowanie plakatu AI dla: {title}...")
        
        # Wywołanie API DALL-E 3
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024", # Proporcje kwadratowe, ale DALL-E generuje świetne grafiki
            quality="standard",
            response_format="url"
        )

        # Pobieramy tymczasowy link od OpenAI
        temp_url = response.data[0].url
        
        # Aby plakat nie zniknął po godzinie, pobieramy go z tymczasowego URL-a
        # i konwertujemy na ContentFile gotowy do zapisu przez Django
        img_response = requests.get(temp_url)
        if img_response.status_code == 200:
            print(f"✓ Wygenerowano plakat AI dla {title}. Pobieram do MEDIA_ROOT...")
            
            # Generujemy unikalną nazwę pliku
            file_name = f"ai_poster_{title.replace(' ', '_')}_{year}.png"
            image_content = ContentFile(img_response.content, name=file_name)
            return image_content, file_name # Zwracamy plik do MEDIA oraz nazwę jako zapasowy URL
            
    except Exception as e:
        print(f"❌ Krytyczny błąd generowania AI lub pobierania dla {title}: {e}")
    
    return None, None

@login_required
def add_movie(request):
    """Dodawanie filmu - tu uruchamiamy AI"""
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.user = request.user
            
            # Najpierw zapisujemy metadane
            movie.save()
            
            # Jeśli user nie wgrał własnego obrazka ani nie podał URL-a
            if not movie.cover and not movie.poster_url:
                # Uruchamiamy generowanie AI, podając tytuł, reżysera i rok z formularza
                ai_image_content, file_name = generate_ai_poster(
                    movie.title, 
                    movie.director, 
                    movie.year
                )
                
                # Jeśli generowanie się udało
                if ai_image_content:
                    # Przypisujemy wygenerowany plik bezpośrednio do pola ImageField ('cover')
                    # Django automatycznie zapisze go w MEDIA_ROOT i stworzy link do MEDIA_URL
                    movie.cover.save(file_name, ai_image_content, save=True)
                    movie.poster_url = None # Czyścimy zapasowe pole URL, żeby nie mąciło
                
            return redirect('movie_list')
    else:
        form = MovieForm()
    return render(request, 'add_movie.html', {'form': form})

# Pozostałe widoki pozostają bez zmian (tylko movie_list ma drobną optymalizację)

@login_required
def movie_list(request):
    search_query = request.GET.get('q', '')
    if search_query:
        movies = Movie.objects.filter(user=request.user, title__icontains=search_query)
    else:
        movies = Movie.objects.filter(user=request.user)
    
    # Nie generujemy AI w pętli przy ładowaniu listy, bo to zamuli stronę na amen.
    # AI działa tylko przy dodawaniu filmu (add_movie).

    return render(request, 'movie_list.html', {'movies': movies, 'search_query': search_query})

@login_required
def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk, user=request.user)
    return render(request, 'movie_detail.html', {'movie': movie})

@login_required
def edit_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk, user=request.user)
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('movie_detail', pk=pk)
    else:
        form = MovieForm(instance=movie)
    return render(request, 'edit_movie.html', {'form': form, 'movie': movie})

@login_required
def delete_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk, user=request.user)
    if request.method == "POST":
        movie.delete()
        return redirect('movie_list')
    return render(request, 'delete_movie.html', {'movie': movie})

@login_required
def global_movies(request):
    movies = GlobalMovie.objects.all()
    user_movies = Movie.objects.filter(user=request.user, global_movie__isnull=False)
    collection_ids = list(user_movies.filter(has_movie=True).values_list('global_movie_id', flat=True))
    wishlist_ids = list(user_movies.filter(wishlist=True).values_list('global_movie_id', flat=True))
    
    return render(request, 'global_movies.html', {
        'global_movies': movies,
        'collection_ids': collection_ids,
        'wishlist_ids': wishlist_ids,
    })

@login_required
def add_global_movie(request, movie_id):
    # Logika dla Katalogu (Discover) zostaje stara, bo tu nie generujemy AI,
    # tylko przypisujemy filmy z gotowego katalogu (o ile mają plakaty).
    # Generowanie AI działa tylko przy dodawaniu własnego filmu przez 'add_movie'.
    global_movie = get_object_or_404(GlobalMovie, id=movie_id)
    movie, created = Movie.objects.get_or_create(
        user=request.user, 
        global_movie=global_movie,
        defaults={
            'title': global_movie.title,
            'director': global_movie.director,
            'year': global_movie.year,
            'genre': global_movie.genre,
            'poster_url': global_movie.poster_url,
        }
    )
    movie.has_movie = True
    movie.wishlist = False
    movie.save()
    return redirect('global_movies')

@login_required
def add_to_wishlist(request, movie_id):
    global_movie = get_object_or_404(GlobalMovie, id=movie_id)
    movie, created = Movie.objects.get_or_create(
        user=request.user, 
        global_movie=global_movie,
        defaults={
            'title': global_movie.title,
            'director': global_movie.director,
            'year': global_movie.year,
            'genre': global_movie.genre,
            'poster_url': global_movie.poster_url,
        }
    )
    movie.wishlist = True
    movie.has_movie = False
    movie.save()
    return redirect('global_movies')

@login_required
def delete_from_catalog(request, movie_id):
    movie = Movie.objects.filter(user=request.user, global_movie_id=movie_id).first()
    if movie:
        movie.delete()
    return redirect('global_movies')