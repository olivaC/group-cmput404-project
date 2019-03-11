from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserCreateForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, )
    last_name = forms.CharField(max_length=30, )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2',)


class LoginForm(forms.Form):
    """
    Form used to log in to the web application.
    """
    username = forms.CharField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label="Username")
    password = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)),
                               label="Password")

    class Meta:
        fields = ['username', 'password']

    def clean(self):
        try:
            User.objects.get(username__iexact=self.cleaned_data['username'])
            user = authenticate(username=self.cleaned_data['username'], password=self.cleaned_data['password'])
            if user is not None:
                if not user.is_authenticated:
                    raise forms.ValidationError("Username/password not found.")
            else:
                raise forms.ValidationError("Username/password not found.")
        except User.DoesNotExist:
            raise forms.ValidationError("Username/password not found")
        return self.cleaned_data
