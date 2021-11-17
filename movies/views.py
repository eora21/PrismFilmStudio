from django.shortcuts import render
from .models import Movie, Color
# Create your views here.

def choice(request):
    return render(request, 'movies/choice.html')

def index(request):
    movies = Movie.objects.all()
    context = {
        'movies': movies,
    }
    return render(request, 'movies/index.html', context)