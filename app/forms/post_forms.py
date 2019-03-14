from django.forms import ModelForm, inlineformset_factory
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm

from app.models import Post, Author


class PostCreateForm(ModelForm):
    text = forms.Textarea()
    title = forms.CharField()
    description = forms.CharField()

    class Meta:
        model = Post
        exclude = ('author', 'date_created')


class EditProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username'
        )


class EditBio(UserChangeForm):
    text = forms.Textarea()
    title = forms.CharField()
    description = forms.CharField()

    class Meta:
        model = Author
        fields = (
            'description',
            'github_url',
        )
