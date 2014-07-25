from django.forms import ModelForm
from .models import Post, Comment

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        exclude = ["post"]
