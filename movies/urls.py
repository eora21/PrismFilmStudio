from django.urls import path
from . import views

app_name = "movies"
urlpatterns = [
    path('choice/', views.choice, name="choice"),
    
    path('index/<int:mode>/', views.index, name="index"),
    
    path('detail/<int:movie_pk>', views.detail, name="detail"),
    path('movie_comment/<int:movie_pk>', views.movie_comment, name="movie_comment"),
    
    path('review_create/<int:movie_pk>/', views.review_create, name="review_create"),
    path('review/<int:review_pk>/', views.review, name="review"),
    path('review_comment/<int:review_pk>', views.review_comment, name="review_comment"),
    
    path('usercolor_create/', views.usercolor_create, name="usercolor_create"),
    
    path('voice_process/', views.voice_process, name="voice_process"),
]
