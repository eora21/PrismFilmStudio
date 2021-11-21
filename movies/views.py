from django.http.request import RAISE_ERROR
from django.shortcuts import render,redirect
from .models import Movie, Color, Review, UserColorRecord
from .forms import ReviewCommentForm, ReviewForm, MovieCommentForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_http_methods, require_safe
import math
from django.http import JsonResponse

@login_required
@require_safe
def choice(request):
    return render(request, 'movies/choice.html')

@login_required
@require_safe
def index(request, mode):                                          # mode : Sorted by 2 - TMDB_Grade / 3 - Release Date / 4 - Search Data / 1, 4~ - Coloring
    if not request.user.usercolorrecord_set.all():
        return redirect('movies:choice')
    
    movies = Movie.objects.all()
    
    # Profile Color Create
    colors = request.user.usercolorrecord_set.all()                # Color List
    last_color = colors[len(colors)-1]                             # Picked Color
    colors = reversed(colors)                                      # Color Sort(Recently)
    
    res_movies = []
    
    # Order by TMDB_Grade
    if mode == 2:
        for movie in movies:
            score = movie.naver_grade
            res_movies.append([movie, score])
    
    # Order by Release Date
    elif mode == 3:
        for movie in movies:
            score = movie.release_date
            res_movies.append([movie, score])
    
    # Order by Search
    elif mode == 4:
        datas = request.GET['searchData'].split()                      # Input Data list
        for movie in movies:                                           # query in title : +10, query in overview +1
            temp_cnt = 0
            title = movie.title
            overview = movie.overview
            for data in datas:
                if data in title:
                    temp_cnt += 10
                if data in overview:
                    temp_cnt += 1
            if temp_cnt >= 1:                                          # If query in title, content, Can be Searched
                res_movies.append([movie,temp_cnt])

    # Order by Coloring
    else:
        last_color_rgb = last_color.color[4:-1].split(", ")            # Users R, G, B list

        for movie in movies:
            movie_color = movie.color_set.all()[0]
            score = math.sqrt(
                    math.pow(int(last_color_rgb[0]) - int(movie_color.color_1_R), 2) +\
                    math.pow(int(last_color_rgb[1]) - int(movie_color.color_1_G), 2) +\
                    math.pow(int(last_color_rgb[2]) - int(movie_color.color_1_B), 2)
                ) + \
            math.sqrt(
                    math.pow(int(last_color_rgb[0]) - int(movie_color.color_2_R), 2) +\
                    math.pow(int(last_color_rgb[1]) - int(movie_color.color_2_G), 2) +\
                    math.pow(int(last_color_rgb[2]) - int(movie_color.color_2_B), 2)
                ) + \
            math.sqrt(
                    math.pow(int(last_color_rgb[0]) - int(movie_color.color_3_R), 2) +\
                    math.pow(int(last_color_rgb[1]) - int(movie_color.color_3_G), 2) +\
                    math.pow(int(last_color_rgb[2]) - int(movie_color.color_3_B), 2)
            ) + \
            math.sqrt(
                    math.pow(int(last_color_rgb[0]) - int(movie_color.color_4_R), 2) +\
                    math.pow(int(last_color_rgb[1]) - int(movie_color.color_4_G), 2) +\
                    math.pow(int(last_color_rgb[2]) - int(movie_color.color_4_B), 2)
                ) + \
            math.sqrt(
                    math.pow(int(last_color_rgb[0]) - int(movie_color.color_5_R), 2) +\
                    math.pow(int(last_color_rgb[1]) - int(movie_color.color_5_G), 2) +\
                    math.pow(int(last_color_rgb[2]) - int(movie_color.color_5_B), 2)
                )
            res_movies.append([movie, int(score)])
    
    if mode == 2 or mode == 3 or mode == 4:
        res_movies.sort(key= lambda x: x[1], reverse=True)
    else:
        res_movies.sort(key= lambda x: x[1])
    
    context = {
        'movies': res_movies,
        'last_color': last_color,
        'colors': colors,
        'mode': mode,
    }
    return render(request, 'movies/index.html', context)

@login_required
@require_safe
def detail(request, movie_pk):
    if not request.user.usercolorrecord_set.all():
        return redirect('movies:choice')
    
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
    return redirect('movies:index', 1)


def voice_process(request):
    data = request.GET['data']
    responsable = {"메인": 1, "매인": 1, "색체": 1, "색체": 1, "평점": 2, "최신": 3, "검색": 4, "뒤로":5, "로그": 6}
    res, query = 0, ""
    
    for key, value in responsable.items():
        if key in data:
            if key == "검색":
                query = str(data[1:data.index("검색")])
            res = value
            break
        
    context = {
        'res' : res,
        'query' : query,
    }
    return JsonResponse(context)