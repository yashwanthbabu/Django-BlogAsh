from django.forms import ModelForm
from django import forms
from django.forms import widgets

from .models import Comment


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        exclude = ["post"]
    

class CommentsForm(forms.Form):
    Author = forms.CharField(widget=forms.TextInput(attrs={'size':'48', 'class':'form-control'}))
    # A CharField that checks that the value is a valid email address.
    email = forms.EmailField(widget=forms.TextInput(attrs={'size':'48', 'class':'form-control'}))
    Body = forms.CharField(widget=forms.Textarea(attrs={'cols':50, 'rows': 5 , 'class':'form-control'}))


class PostForm(forms.Form):
    title = forms.CharField(max_length=50)
    body = forms.CharField(widget=forms.Textarea, required=False)
