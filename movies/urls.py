from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('', views.movie_list, name='movie_list'),
    path('movie/<int:pk>/', views.movie_detail, name='movie_detail'),
    path('add/', views.add_movie, name='add_movie'),
    path('edit/<int:pk>/', views.edit_movie, name='edit_movie'),
    path('delete/<int:pk>/', views.delete_movie, name='delete_movie'),
    path('discover/', views.global_movies, name='global_movies'),
    path('add-from-global/<int:movie_id>/', views.add_global_movie, name='add_global_movie'),
    path('add-wishlist/<int:movie_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('delete-from-collection/<int:movie_id>/', views.delete_from_catalog, name='delete_from_catalog'),
    
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]