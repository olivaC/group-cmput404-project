from django.forms import ModelForm
from django import forms

from app.models import Post


class PostCreateForm(ModelForm):
    text = forms.Textarea()
    title = forms.CharField()
    description = forms.CharField()

    class Meta:
        model = Post
        exclude = ('author', 'date_created',)
