from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


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


class RegistrationForm(forms.Form):
    username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Username"), error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") })
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Email address"))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Password (again)"))
 
    def clean_username(self):
        try:
            User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_("The username already exists."))

    def clean_email(self):
        try:
            User.objects.get(email=self.cleaned_data['email'])
            raise forms.ValidationError("This email already exist")
        except User.DoesNotExist:
            return self.cleaned_data['email']
 
    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields did not match."))
        return self.cleaned_data
    