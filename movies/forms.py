from django.db.models.base import Model
from django.forms import ModelForm
from .models import MovieComment, Review, ReviewComment

class MovieCommentForm(ModelForm):
    class Meta:
        model = MovieComment
        fields = ('grade', 'content')
        
class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ('title','content')
        
class ReviewCommentForm(ModelForm):
    class Meta:
        model = ReviewComment
        fields = '__all__'