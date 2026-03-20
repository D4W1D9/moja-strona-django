from django.contrib import admin
from .models import Movie, GlobalMovie

@admin.register(GlobalMovie)
class GlobalMovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'director', 'year', 'genre', 'created_at')
    search_fields = ('title', 'director', 'genre')
    list_filter = ('year', 'genre', 'created_at')
    ordering = ('-created_at',)

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_user', 'director', 'year', 'has_movie', 'rating')
    search_fields = ('title', 'director', 'user__username')
    list_filter = ('has_movie', 'media_type', 'year', 'created_at')
    ordering = ('-created_at',)
    
    def get_user(self, obj):
        return obj.user.username if obj.user else 'Global'
    get_user.short_description = 'User'
