from django.shortcuts import render,redirect
from .models import Movie, Color, Review
from .forms import ReviewCommentForm, ReviewForm, MovieCommentForm
# Create your views here.

def choice(request):
    return render(request, 'movies/choice.html')

def index(request):
    movies = Movie.objects.all()
    context = {
        'movies': movies,
    }
    return render(request, 'movies/index.html', context)

def detail(request, movie_pk):
    movie = Movie.objects.get(id = movie_pk)
    color = movie.color_set.all()
    context = {
        'movie': movie,
        'color': color,
    }
    return render(request,'movies/detail.html', context)

def movie_comment(request, movie_pk):
    movie = Movie.objects.get(pk = movie_pk)
    form = MovieCommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.movie = movie
        comment.user = request.user
        comment.save()
        return redirect('movies:detail', movie_pk)
    return redirect('movies:detail', movie_pk)


def review_create(request, movie_pk):
    movie = Movie.objects.get(pk = movie_pk)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.user = request.user
            review.save()
            return redirect('movies:detail', movie_pk)
    else:
        form = ReviewForm()
    context = {
        'form': form
    }
    return render(request, 'movies/review_create.html', context)

def review(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    context = {
        'review': review,
    }
    return render(request,'movies/review.html', context)
    

def review_comment(request, review_pk):
    pass