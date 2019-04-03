import requests
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.forms import model_to_dict
from django.views.decorators.csrf import csrf_exempt, requires_csrf_token
from django.http import HttpResponse

from app.models import *
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test

# Create your views here.
from django.urls import reverse

from SocialDistribution import settings
from app.forms.post_forms import EditProfileForm, EditBio
from app.forms.registration_forms import LoginForm, UserCreateForm
from app.utilities import *
from app.views import gh_stream


@login_required
@user_passes_test(api_check)
@requires_csrf_token
def index(request):
    user = request.user
    print(user.user.id)
    request.context['user'] = user
    friends = request.user.user.friends.all()
    foaf_friends = set()
    if friends:
        for i in friends:
            foaf = i.friends.all()
            for j in foaf:
                foaf_friends.add(j.id)

    posts = Post.objects.all().filter(author__id__in=request.user.user.friends.all()).filter(
        visibility="FRIENDS") | Post.objects.all().filter(author__id__in=request.user.user.friends.all()).filter(
        visibility="SERVERONLY") | Post.objects.all().filter(author__id__in=request.user.user.friends.all()).filter(
        visibility="FOAF") | Post.objects.all().filter(author=user.user) | Post.objects.all().filter(
        visibility="PUBLIC") | Post.objects.all().filter(author__id__in=foaf_friends).filter(visibility="FOAF")

    gh_activities = []
    if user.user.github_url:
        author = Author.objects.get(id=user.user.id)
        gh_activities = gh_stream.get_activities(author, 5, 10)
        posts = list(posts) + gh_activities
    else:
        posts = list(posts.order_by('-published'))

    servers = Server.objects.all()
    public_posts = list()

    for server in servers:
        host = server.hostname
        if not server.hostname.endswith("/"):
            host = server.hostname + "/"
        server_api = "{}posts".format(host)
        try:
            if server.username and server.password:
                r = requests.get(server_api, auth=(server.username, server.password))
            else:
                r = requests.get(server_api)

            p = create_posts(r.json())
            public_posts.extend(p)
        except:
            print("error")

    posts = public_posts + list(posts)
    posts.sort(key=lambda post: post.published, reverse=True)

    request.context['posts'] = posts

    # print(public_posts)

    return render(request, 'index.html', request.context)


@login_required
@user_passes_test(api_check)
def profile_view(request, id=None):
    author = get_object_or_404(Author, id=id)
    request.context['author'] = author
    current_user = get_object_or_404(Author, username=request.user)
    request.context['self'] = current_user
    try:
        f_request = FriendRequest.objects.all().filter(author=current_user).values('friend')
        pending = Author.objects.all().filter(id__in=f_request)

        request.context['pending'] = pending

        friends = request.user.user.friends.all()
        request.context['friends'] = friends
    except:
        print('error remote user')
        return HttpResponseRedirect('index.html')

    return render(request, 'profile.html', request.context)


@login_required
@user_passes_test(api_check)
def edit_profile(request):
    user = request.user
    author = request.user.user
    try:
        if request.method == 'POST':
            edit_form = EditProfileForm(request.POST)
            bio_form = EditBio(request.POST)

            if edit_form.is_valid():
                user.first_name = edit_form.cleaned_data.get('first_name')
                user.last_name = edit_form.cleaned_data.get('last_name')

                if bio_form.is_valid():
                    # bio_form.save()
                    author.bio = bio_form.cleaned_data.get('bio')
                    author.github_url = bio_form.cleaned_data.get('github_url')
                    author.username = bio_form.data.get('username')
                    author.save()
                    user.username = bio_form.cleaned_data.get('username')
                elif bio_form.data.get('username') == author.username:
                    author.bio = bio_form.cleaned_data.get('bio')
                    author.github_url = bio_form.cleaned_data.get('github_url')
                    author.save()
                else:
                    author.bio = bio_form.cleaned_data.get('bio')
                    author.github_url = bio_form.cleaned_data.get('github_url')
                    author.username = bio_form.data.get('username')
                    author.save()
                    user.username = bio_form.data.get('username')

                user.save()
                redirect('app:index')

    except Exception as e:
        messages.warning(request, 'Error update')

    user_form = EditProfileForm(initial=model_to_dict(user))
    form = EditBio(initial=model_to_dict(author))
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
                user = User.objects.create_user(
                    form.cleaned_data['username'],
                    password=form.cleaned_data.get('password1')
                )
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.is_active = False
                user.save()
                messages.success(request,
                                 'You have signed up successfully! Please wait for the admin to approved your account')
                # user = authenticate(username=user.username, password=form.cleaned_data.get('password1'))
                # login(request, user)
                return HttpResponseRedirect(reverse('app:index'))
            else:
                messages.success(request,
                                 'Sign up error')

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
@user_passes_test(api_check)
@csrf_exempt
def get_image(request, filename):
    """
        View for getting an image

        :param request
        :return: 404 if image does not exist, 403 if no permission and image file if success
    """
    post = Post.objects.get(id=filename)
    baseIndex = post.content.find(";base64,")
    mimeType = post.content[5:baseIndex]
    data = get_image_from_base64(post.content[baseIndex + 8:])
    return HttpResponse(data, content_type=mimeType)


@login_required
@user_passes_test(api_check)
def search_view(request, username=None):
    queryset_list = Author.objects.all()
    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(username__icontains=query)

    else:
        return HttpResponseRedirect('/search/')

    request.context['authors'] = queryset_list

    return render(request, 'search_author.html', request.context)


@login_required
@requires_csrf_token
def api_test(request):
    request.context['domain'] = DOMAIN
    return render(request, 'api_test.html', request.context)
