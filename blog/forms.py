from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Comment


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        exclude = ["post"]


class CommentsForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'size': '48',
                           'class': 'form-control'}))
    # A CharField that checks that the value is a valid email address.
    email = forms.EmailField(widget=forms.TextInput(attrs={'size': '48',
                             'class': 'form-control'}))
    Body = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 5,
                           'class': 'form-control'}))


class PostForm(forms.Form):
    title = forms.CharField(max_length=50)
    body = forms.CharField(widget=forms.Textarea, required=False)


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'size': '48',
                             'class': 'form-control'}))
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)


class MyRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    birtday = forms.DateField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(MyRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['First name']
        user.last_name = self.cleaned_data['Last name']
        user.birthday = self.cleaned_data['Birthday']
        if commit:
            user.save()

        return user
