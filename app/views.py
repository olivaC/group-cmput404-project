from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Author



def index(request, username):
    return render(request, 'index.html')

def register(request):
	return render(request, 'register.html')

def login(request):
    return render(request, 'login.html')

def verify_register(request):
    username = request.POST['username']

    if(request.POST['submit'] == "Register Account"):
        try:
            author = Author.objects.get(username=username)
        except (Author.DoesNotExist):
            author = Author(username=username)
            author.save()
            return HttpResponseRedirect(reverse('app:index', args=(username,)))
        else:
            return render(request, 'register.html', {'error_message': "This username already exists. Please use a different username."})

    elif(request.POST['submit'] == "Already have an account? Login!"):
        return HttpResponseRedirect(reverse('app:login', args=()))

def verify_login(request):
    if(request.GET['submit'] == "Login"):
        username = request.GET['username']
        try:
            author = Author.objects.get(username=username)
        except (Author.DoesNotExist):
            return render(request, 'login.html', {'error_message': "This username does not exists. Please try again."})
        else:
            return HttpResponseRedirect(reverse('app:index', args=(username,)))

    elif(request.GET['submit'] == "Create an Account!"):
        return HttpResponseRedirect(reverse('app:register', args=()))