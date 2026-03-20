from django.contrib import admin
from django.urls import path
from main.views import home
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('o-mnie/', views.o_mnie, name='o_mnie'),
    path('projekty/', views.projekty, name='projekty'),
    path('kontakt/', views.kontakt, name='kontakt'),
    path('design/', views.design, name='design'),
    path('python-power/', views.python_power, name='python_power'),
    path('szybki-start/', views.szybki_start, name='szybki_start'),
]