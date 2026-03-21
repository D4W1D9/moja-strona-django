from django import forms
from .models import Movie

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'director', 'year', 'genre', 'has_movie', 'media_type', 'rating', 'notes', 'cover', 'poster_url']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'np. Incepcja'}),
            'director': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'np. Christopher Nolan'}),
            'year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '2010'}),
            'genre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sci-Fi, Akcja'}),
            'media_type': forms.Select(attrs={'class': 'form-control'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 10}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'poster_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Wklej link do obrazka z Google (opcjonalne)'}),
        }