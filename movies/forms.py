from django import forms
from .models import Movie

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'director', 'year', 'genre', 'has_movie', 'media_type', 'rating', 'notes', 'cover']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Inception'}),
            'director': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Christopher Nolan'}),
            'year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '2010'}),
            'genre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sci-Fi, Action'}),
            'media_type': forms.Select(attrs={'class': 'form-control'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 10}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }