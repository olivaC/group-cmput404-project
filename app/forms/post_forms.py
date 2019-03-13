from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm

from app.models import Post


class PostCreateForm(ModelForm):
    text = forms.Textarea()

    class Meta:
        model = Post
        exclude = ('author', 'date_created', 'private')


class EditProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username'
        )
