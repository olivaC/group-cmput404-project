from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from app.models import *
import mimetypes
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.urls import reverse

from SocialDistribution import settings
from app.forms.post_forms import PostCreateForm, EditProfileForm, EditBio
from app.forms.registration_forms import LoginForm, UserCreateForm
from app.models import Post, Author
from app.utilities import unquote_redirect_url


@login_required
def index(request):
    user = request.user
    request.context['user'] = user

    posts = Post.objects.all().filter(author=user.user).order_by('-id')

    if request.method == 'POST':
        next = request.POST.get("next", reverse("app:index"))
        form = PostCreateForm(request.POST)
        try:
            if form.is_valid():
                if form.cleaned_data.get('text'):
                    Post.objects.create(author=user.user, text=form.cleaned_data.get('text'))
                    return HttpResponseRedirect(reverse('app:index'))
            request.context['next'] = next
            messages.warning(request, 'Cannot post something empty!')


        except:
            request.context['next'] = request.GET.get('next', reverse("app:index"))

    form = PostCreateForm()
    request.context['form'] = form
    request.context['posts'] = posts

    return render(request, 'index.html', request.context)


@login_required
def my_posts_view(request):
    user = request.user
    request.context['user'] = user

    posts = Post.objects.all().filter(author=user.user).order_by('-id')

    if request.method == 'POST':
        next = request.POST.get("next", reverse("app:index"))
        form = PostCreateForm(request.POST)
        try:
            if form.is_valid():
                if form.cleaned_data.get('text'):
                    Post.objects.create(author=user.user, text=form.cleaned_data.get('text'))
                    return HttpResponseRedirect(reverse('app:index'))
            request.context['next'] = next
            messages.warning(request, 'Cannot post something empty!')


        except:
            request.context['next'] = request.GET.get('next', reverse("app:index"))

    form = PostCreateForm()
    request.context['form'] = form
    request.context['posts'] = posts

    return render(request, 'myposts.html', request.context)


def delete_post(request, id=None):
    post = get_object_or_404(Post, id=id)

    try:
        if request.method == 'POST':
            form = PostCreateForm(request.POST)
            post.delete()
            # messages.success(request, 'Post deleted')
            return redirect('../../my-posts')
            # return redirect('../../')

    except Exception as e:
        messages.warning(request, 'Post could not be deleted')

    form = PostCreateForm()
    request.context['form'] = form

    return render(request, 'post_delete.html', request.context)


@login_required
def profile_view(request):
    user = request.user
    author = get_object_or_404(Author, user=user)
    args = {'author': author}

    return render(request, 'profile.html', args)


def edit_profile(request):
    user = request.user
    author = get_object_or_404(Author, user=user)
    try:
        if request.method == 'POST':
            edit_form = EditProfileForm(request.POST)
            bio_form = EditBio(request.POST)

            if edit_form.is_valid():
                user.first_name = edit_form.cleaned_data.get('first_name')
                user.last_name = edit_form.cleaned_data.get('last_name')

                if bio_form.is_valid():
                    bio_form.save()
                    user.username = bio_form.cleaned_data.get('username')
                elif bio_form.data.get('username') == author.username:
                    author.bio = bio_form.cleaned_data.get('bio')
                    author.github_url = bio_form.cleaned_data.get('github_url')
                    author.save()

                user.save()

                return redirect('/profile')

    except Exception as e:
        messages.warning(request, 'Error update')

    user_form = EditProfileForm(instance=user)
    form = EditBio(instance=author)
    args = {'bio_form': form,
            'user_form': user_form
            }
    return render(request, 'edit_profile.html', args)


def register_view(request):
    if request.method == 'POST':
        next = request.POST.get("next", reverse("app:index"))
        form = UserCreateForm(request.POST)
        try:
            if form.is_valid():
                user = form.save(request.POST)
                user.username = form.cleaned_data['username']
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.save()
                user = authenticate(username=user.username, password=form.cleaned_data.get('password1'))
                login(request, user)
                return HttpResponseRedirect(reverse('app:index'))
            request.context['next'] = next
        except:
            request.context['next'] = request.GET.get('next', reverse("app:index"))
    else:
        form = UserCreateForm()
        request.context['next'] = request.GET.get('next', reverse("app:index"))
    request.context['form'] = form
    return render(request, 'register.html', request.context)


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        try:
            if form.is_valid():
                user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
                login(request, user)
                redirect_url = request.POST.get('next', reverse("app:index"))
                return HttpResponseRedirect(unquote_redirect_url(redirect_url))
            else:
                request.context['next'] = unquote_redirect_url(request.GET.get('next', reverse("app:index")))
        except:
            request.context['next'] = unquote_redirect_url(request.GET.get('next', reverse("app:index")))

    else:
        request.context['next'] = request.GET.get('next', '')
        form = LoginForm()
    request.context['form'] = form
    request.context['path'] = settings.DOMAIN
    return render(request, 'login.html', request.context)


@login_required
def logout_view(request):
    """
    View used for logging out.

    :param request:
    :return: The index page.
    """
    logout(request)
    return HttpResponseRedirect(request.GET.get(next, reverse("app:index")))


@login_required
@csrf_exempt
def upload_image_view(request):
    """
    View for uploading an image

    :param request
    :return: 200 or 500
    """
    if request.method == 'POST':
        imageForm = ImageForm(request.POST, request.FILES)
        if imageForm.is_valid():
            image = Image()
            image.author = Author.objects.get(user=request.user)
            image.private = int(request.POST.get("private", "0"))
            image.file = request.FILES["file"]
            image.save()
            return HttpResponse("True")
        else:
            return HttpResponse("Not Valid: " + str(imageForm.errors), status=500)
    else:
        return HttpResponse("Must be Post", status=500)


@csrf_exempt
def get_image(request, username, filename):
    """
        
    """
    try:
        path = Image.get_image_dir(username, filename)
        mimeType = mimetypes.guess_type(path)[0]
        image = Image.objects.get(file=path)
        if image.private:
            # TODO Check is Friend
            return HttpResponse(status=403)
        with open(path, "rb") as file:
            return HttpResponse(file.read(), content_type=mimeType)
    except:
        return HttpResponse(status=404)


@login_required
def create_post_view(request):
    user = request.user
    request.context['user'] = user

    if request.method == 'POST':
        next = request.POST.get("next", reverse("app:index"))
        form = PostCreateForm(request.POST)
        try:
            if form.is_valid():
                if form.cleaned_data.get('text'):
                    Post.objects.create(author=user.user, text=form.cleaned_data.get('text'),
                                        description=form.cleaned_data.get('description'),
                                        title=form.cleaned_data.get('title'), privacy=form.cleaned_data.get('privacy'))
                    return HttpResponseRedirect(reverse('app:index'))
            request.context['next'] = next
            messages.warning(request, 'Cannot post something empty!')


        except:
            request.context['next'] = request.GET.get('next', reverse("app:index"))

    form = PostCreateForm()
    request.context['form'] = form

    return render(request, 'create_post.html', request.context)
