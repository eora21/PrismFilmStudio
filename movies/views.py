from django.shortcuts import render,redirect
from .models import Movie, Color, Review, UserColorRecord
from .forms import ReviewCommentForm, ReviewForm, MovieCommentForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_http_methods, require_safe
# Create your views here.

@login_required
@require_safe
def choice(request):
    return render(request, 'movies/choice.html')

@login_required
# @require_safe
def index(request):
    movies = Movie.objects.all()
    
    # Profile Color Create
    colors = request.user.usercolorrecord_set.all()                # Color List
    last_color = colors[len(colors)-1]                             # Picked Color
    colors = reversed(colors)                                      # Color Sort(Recently)
        
    context = {
        'movies': movies,
        'last_color': last_color,
        'colors': colors,
    }
    return render(request, 'movies/index.html', context)

@login_required
# @require_safe
def detail(request, movie_pk):
    movie = Movie.objects.get(id = movie_pk)
    
    # Profile Color Create
    colors = request.user.usercolorrecord_set.all()                # Color List
    last_color = colors[len(colors)-1]                             # Picked Color
    colors = reversed(colors)                                      # Color Sort(Recently)
    
    context = {
        'movie': movie,
        'colors': colors,
        'last_color': last_color,
    }
    return render(request,'movies/detail.html', context)

@login_required
@require_http_methods(['GET','POST'])
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


@login_required
@require_http_methods(['GET','POST'])
def review_create(request, movie_pk):
    movie = Movie.objects.get(pk = movie_pk)
    
    # Profile Color Create
    colors = request.user.usercolorrecord_set.all()                # Color List
    last_color = colors[len(colors)-1]                             # Picked Color
    colors = reversed(colors)                                      # Color Sort(Recently)
    
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
        'movie': movie,
        'form': form,
        'last_color': last_color,
        'colors': colors,
    }
    return render(request, 'movies/review_create.html', context)

@login_required
@require_safe
def review(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    
    # Profile Color Create
    colors = request.user.usercolorrecord_set.all()                # Color List
    last_color = colors[len(colors)-1]                             # Picked Color
    colors = reversed(colors)                                      # Color Sort(Recently)
    
    context = {
        'review': review,
        'last_color': last_color,
        'colors': colors,
    }
    return render(request,'movies/review.html', context)
    

@require_POST
def review_comment(request, review_pk):
    if not request.user.is_authenticated:
        return redirect('movies:review', review_pk)
    
    review = Review.objects.get(pk = review_pk)
    if request.method == "POST":
        form = ReviewCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.review = review
            comment.save()
            return redirect('movies:review', review_pk)
            
    return redirect('movies:review', review_pk)
        

@require_POST
def usercolor_create(request):
    colors = request.user.usercolorrecord_set.all()
    if len(colors) >= 5:                                                            # Maintain Color Up to 5
        colors[0].delete()
    UserColorRecord.objects.create(user=request.user, color=request.POST['color'])  # Color Push
    return redirect('movies:index')