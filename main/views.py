from django.shortcuts import render

def home(request):
    cards = [
        {"title": "Nowoczesny Design", "desc": "Czysty kod i świetne animacje."},
        {"title": "Moc Pythona", "desc": "Backend napędzany przez Django."},
        {"title": "Szybki Start", "desc": "Gotowe do wdrożenia w kilka minut."}
    ]
    return render(request, 'index.html', {'cards': cards})
