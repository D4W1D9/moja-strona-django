from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie
from .forms import MovieForm

def movie_list(request):
    # Pobieramy to, co użytkownik wpisał w wyszukiwarkę
    query = request.GET.get('q')
    
    if query:
        # Jeśli coś wpisał, filtrujemy po tytule (icontains = zawiera, ignoruje wielkość liter)
        movies = Movie.objects.filter(title__icontains=query).order_by('-created_at')
    else:
        # Jeśli nic nie wpisał, pokazujemy wszystko
        movies = Movie.objects.all().order_by('-created_at')
    
    context = {
        'movies': movies,
        'search_query': query, # Przekazujemy to do HTMLa, żeby zostawić wpisany tekst w polu
    }
    return render(request, 'movie_list.html', context)

def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('movie_list')
    else:
        form = MovieForm()
    return render(request, 'add_movie.html', {'form': form, 'page_title': 'Add New Movie'})

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    return render(request, 'movie_detail.html', {'movie': movie})

def edit_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('movie_detail', movie_id=movie.id)
    else:
        form = MovieForm(instance=movie)
    return render(request, 'add_movie.html', {'form': form, 'page_title': f'Edit Movie: {movie.title}'})

def delete_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if request.method == 'POST':
        movie.delete()
        return redirect('movie_list')
    return render(request, 'delete_movie.html', {'movie': movie})