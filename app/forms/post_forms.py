from django.forms import ModelForm, inlineformset_factory
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm

from app.models import Post, Author, Comment

class AuthorForm(ModelForm):
    author_id = forms.CharField()
    host = forms.CharField(label="hello")
    displayName = forms.CharField()
    url = forms.CharField()

    class Meta:
        model = Author
        fields = (
            'author_id',
            'host',
            'displayName',
            'url',
            )

class PostCreateForm(ModelForm):
    content = forms.Textarea()
    title = forms.CharField()
    description = forms.CharField()

    class Meta:
        model = Post
        exclude = ('author', 'published')


class EditProfileForm(ModelForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
        )


class EditBio(ModelForm):
    username = forms.CharField()

    class Meta:
        model = Author
        fields = (
            'username',
            'bio',
            'github_url',
        )


class CommentCreateForm(ModelForm):
    comment = forms.Textarea()

    class Meta:
        model = Comment
        exclude = (
            'post',
            'author',
            'published'
        )
