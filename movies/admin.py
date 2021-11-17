from django.contrib import admin
from .models import Movie, Color, MovieComment, Review, ReviewComment

# Register your models here.
admin.site.register(Movie)
admin.site.register(Color)
admin.site.register(MovieComment)
admin.site.register(Review)
admin.site.register(ReviewComment)