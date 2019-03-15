from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import model_to_dict
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from SocialDistribution import settings
from app.forms.post_forms import PostCreateForm
from app.models import Post


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

    return render(request, 'posts/my_posts.html', request.context)


def delete_post(request, id=None):
    post = get_object_or_404(Post, id=id)

    try:
        if request.method == 'POST':
            form = PostCreateForm(request.POST)
            post.delete()
            # messages.success(request, 'Post deleted')
            return redirect('../../my-posts')

    except Exception as e:
        messages.warning(request, 'Post could not be deleted')

    form = PostCreateForm()
    request.context['form'] = form

    return render(request, 'posts/post_delete.html', request.context)


def edit_post(request, id=None):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        next = request.POST.get("next", reverse("app:my_posts"))
        form = PostCreateForm(request.POST)
        if form.is_valid():
            post.title = form.cleaned_data.get('title')
            post.description = form.cleaned_data.get('description')
            post.privacy = form.cleaned_data.get('privacy')
            post.text = form.cleaned_data.get('text')
            post.save()
            return HttpResponseRedirect(reverse('app:my_posts'))

        else:
            messages.warning(request, 'Error editing your post')

    form = PostCreateForm(initial=model_to_dict(post))
    request.context['post'] = post
    request.context['form'] = form

    return render(request, 'posts/edit_post.html', request.context)


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

    return render(request, 'posts/create_post.html', request.context)
