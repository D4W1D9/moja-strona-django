from django.shortcuts import render

def home(request):
    return render(request, 'index.html')

def o_mnie(request):
    return render(request, 'o_mnie.html')

def projekty(request):
    return render(request, 'projekty.html')

def kontakt(request):
    return render(request, 'kontakt.html')

def design(request):
    return render(request, 'design.html')

def python_power(request):
    return render(request, 'python_power.html')

def szybki_start(request):
    return render(request, 'szybki_start.html')