from django.db import models

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=50)
    overview = models.TextField()
    poster_url = models.TextField(null=True)
    naver_grade = models.FloatField(null=True)
    release_date = models.TextField()
    
    def __str__(self):
        return self.title

class Color(models.Model):
    movie = models.ForeignKey(Movie, verbose_name="color", on_delete=models.CASCADE)
    color = models.CharField(max_length=50)
    color_url = models.TextField(null=True)
    color_1_R = models.CharField(max_length=50)
    color_1_G = models.CharField(max_length=50)
    color_1_B = models.CharField(max_length=50)
    color_2_R = models.CharField(max_length=50)
    color_2_G = models.CharField(max_length=50)
    color_2_B = models.CharField(max_length=50)
    color_3_R = models.CharField(max_length=50)
    color_3_G = models.CharField(max_length=50)
    color_3_B = models.CharField(max_length=50)
    color_4_R = models.CharField(max_length=50)
    color_4_G = models.CharField(max_length=50)
    color_4_B = models.CharField(max_length=50)
    color_5_R = models.CharField(max_length=50)
    color_5_G = models.CharField(max_length=50)
    color_5_B = models.CharField(max_length=50)
    
    def __str__(self):
        return self.movie.title