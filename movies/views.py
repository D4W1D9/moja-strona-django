from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.db.models import Q
from .models import Movie, GlobalMovie
from .forms import MovieForm

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        # Sprawdzamy czy hasła się zgadzają
        if password != password_confirm:
            messages.error(request, 'Hasła się nie zgadzają!', extra_tags='error')
            return render(request, 'register.html')
        
        # Sprawdzamy czy użytkownik już istnieje
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Użytkownik już istnieje!', extra_tags='error')
            return render(request, 'register.html')
        
        # Tworzymy nowego użytkownika
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        
        messages.success(request, 'Rejestracja pomyślna! Zaloguj się.', extra_tags='success')
        return redirect('login')
    
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Witaj {username}!', extra_tags='success')
            return redirect('movie_list')
        else:
            messages.error(request, 'Zła nazwa użytkownika lub hasło!', extra_tags='error')
    
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Wylogowano!', extra_tags='success')
    return redirect('login')

@login_required(login_url='login')
def movie_list(request):
    # Pobieramy to, co użytkownik wpisał w wyszukiwarkę
    query = request.GET.get('q')
    
    # Filtrujemy filmy tylko dla zalogowanego użytkownika
    if query:
        movies = Movie.objects.filter(user=request.user, title__icontains=query).order_by('-created_at')
    else:
        movies = Movie.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'movies': movies,
        'search_query': query,
    }
    return render(request, 'movie_list.html', context)

@login_required(login_url='login')
def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.user = request.user  # Przypisujemy film do zalogowanego użytkownika
            movie.save()
            messages.success(request, 'Film dodany!', extra_tags='success')
            return redirect('movie_list')
    else:
        form = MovieForm()
    return render(request, 'add_movie.html', {'form': form, 'page_title': 'Dodaj Film'})

@login_required(login_url='login')
def movie_detail(request, movie_id):
    # Sprawdzamy czy film należy do zalogowanego użytkownika
    movie = get_object_or_404(Movie, id=movie_id, user=request.user)
    return render(request, 'movie_detail.html', {'movie': movie})

@login_required(login_url='login')
def edit_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id, user=request.user)
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            form.save()
            messages.success(request, 'Film zaktualizowany!', extra_tags='success')
            return redirect('movie_detail', movie_id=movie.id)
    else:
        form = MovieForm(instance=movie)
    return render(request, 'add_movie.html', {'form': form, 'page_title': f'Edytuj Film: {movie.title}'})

@login_required(login_url='login')
def delete_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id, user=request.user)
    if request.method == 'POST':
        movie.delete()
        messages.success(request, 'Film usunięty!', extra_tags='success')
        return redirect('movie_list')
    return render(request, 'delete_movie.html', {'movie': movie})

# GLOBAL MOVIES - DOSTĘPNE DLA WSZYSTKICH
def global_movies_list(request):
    """Wyświetl globalną listę filmów"""
    query = request.GET.get('q')
    
    if query:
        global_movies = GlobalMovie.objects.filter(
            Q(title__icontains=query) | Q(director__icontains=query)
        ).order_by('-created_at')
    else:
        global_movies = GlobalMovie.objects.all().order_by('-created_at')
    
    # Sprawdzamy które filmy użytkownik już ma w kolekcji
    user_movie_ids = []
    if request.user.is_authenticated:
        user_movie_ids = list(
            Movie.objects.filter(user=request.user, global_movie__isnull=False)
            .values_list('global_movie_id', flat=True)
        )
    
    context = {
        'global_movies': global_movies,
        'search_query': query,
        'user_movie_ids': user_movie_ids,
    }
    return render(request, 'global_movies.html', context)

@login_required(login_url='login')
def add_global_movie_to_collection(request, global_movie_id):
    """Dodaj film z globalnej listy do kolekcji użytkownika"""
    global_movie = get_object_or_404(GlobalMovie, id=global_movie_id)
    
    # Sprawdzamy czy użytkownik ma już ten film
    existing_movie = Movie.objects.filter(user=request.user, global_movie=global_movie).first()
    
    if existing_movie:
        messages.warning(request, f'Masz już "{global_movie.title}" w swojej kolekcji!', extra_tags='error')
        return redirect('global_movies')
    
    # Tworzymy nowy film w kolekcji użytkownika
    movie = Movie.objects.create(
        user=request.user,
        global_movie=global_movie,
        title=global_movie.title,
        director=global_movie.director,
        year=global_movie.year,
        genre=global_movie.genre,
        cover=global_movie.cover,
    )
    
    messages.success(request, f'"{global_movie.title}" dodany do Twojej kolekcji!', extra_tags='success')
    return redirect('movie_list')