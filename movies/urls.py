from django.urls import path
from . import views

app_name = "movies"
urlpatterns = [
    path('choice/', views.choice, name="choice"),
    path('index/', views.index, name="index"),
]
