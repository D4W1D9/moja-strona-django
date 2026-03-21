from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class GlobalMovie(models.Model):
    """Globalna baza filmów dostępna dla wszystkich użytkowników"""
    title = models.CharField(max_length=255, unique=True)
    director = models.CharField(max_length=255, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    genre = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    cover = models.ImageField(upload_to='global_covers/', blank=True, null=True)
    poster_url = models.URLField(max_length=1000, blank=True, null=True, help_text="Link do plakatu z internetu")
    series_name = models.CharField(max_length=255, blank=True, null=True, help_text="Nazwa serii (np. 'John Wick', 'Terminator')")
    series_order = models.IntegerField(blank=True, null=True, help_text="Numer części w serii (1, 2, 3...)")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['series_name', 'series_order', 'title']

    def __str__(self):
        return f"{self.title} ({self.year})"


class Movie(models.Model):
    MEDIA_CHOICES = [
        ('DVD', 'DVD'),
        ('BR', 'Blu-ray'),
        ('STR', 'Streaming'),
        ('FILE', 'Digital File'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='movies', null=True, blank=True)
    global_movie = models.ForeignKey(GlobalMovie, on_delete=models.SET_NULL, related_name='user_instances', null=True, blank=True)
    
    title = models.CharField(max_length=255)
    director = models.CharField(max_length=255, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    genre = models.CharField(max_length=100, blank=True, null=True)
    
    has_movie = models.BooleanField(default=False, verbose_name="I own this movie")
    media_type = models.CharField(max_length=10, choices=MEDIA_CHOICES, default='STR')
    
    watched = models.BooleanField(default=False, verbose_name="Watched")
    wishlist = models.BooleanField(default=False, verbose_name="On wishlist")
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    cover = models.ImageField(upload_to='covers/', blank=True, null=True)
    poster_url = models.URLField(max_length=1000, blank=True, null=True, help_text="Link do plakatu z internetu")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title