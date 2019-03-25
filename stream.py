#!/usr/bin/env python3
import base64
import mimetypes
from SocialDistribution import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from app.forms.post_forms import PostCreateForm, EditProfileForm, EditBio
from app.forms.registration_forms import LoginForm, UserCreateForm
from app.models import *
from app.utilities import unquote_redirect_url
from datetime import datetime
from datetime import date
from pytz import utc
import github
import pickle
import json
import sys

def put_post(post):
    print('title:', post.title + ' by ' + post.author.username)
    print('published:', post.published)
    print('content:\n' + post.content)
    print('-----------------------------------------------')


posts = []
user = Author.objects.get(username='githuber')
posts = list(Post.objects.all())


gh_events = []
gh_user = github.Github().get_user("skywolff")
events = gh_user.get_events()
# with open('gh_events.data', 'rb') as f:
#      gh_events = pickle.load(f)

today = date.today()
last_year_today = datetime(today.year - 1, today.month, today.day)
for e in events.get_page(page=0):
# for e in gh_events:
    if e.created_at > last_year_today:
        if e.type == 'CreateEvent':
            print(e)
            try:
                title = ''
                description = ''
                visibility = ''
                content = ''

                title = 'Created ' + e.payload['ref_type'] + ' '
                if e.payload['ref_type'] == 'repository':
                    title += e.repo.name 
                elif e.payload['ref_type'] == 'branch':
                    title += e.payload['ref'] + ' on repository ' + e.repo.name
                description = "github event"
                if e.public:
                    visibility = 'PUBLIC'
                else:
                    visibility = 'PRIVATE'

                if e.payload['description']:
                    content += e.payload['description'] + '\n'
                content += 'repo url: ' + e.repo.html_url

                # print(json.dumps(e.raw_data, indent=4))
                # print("title: \t\t",        title)
                # print("created_at: \t",     e.created_at)
                # print("description: \t",    description)
                # print(content)

                # make a post
                new_post = Post(
                    author      = user,
                    published   = e.created_at,
                    title       = title,
                    description = description,
                    visibility  = visibility,
                    content     = content,
                    contentType = 'text/plain'
                )
                put_post(new_post)
            except Exception as exc:
                print("----------------------------------------")
                print("EXCEPTION!!!!")
                print(exc)
                exc_type, exc_obj, tb = sys.exc_info()
                print('lineno =', tb.tb_lineno)
                print("----------------------------------------")
                # print(json.dumps(e.raw_data, indent=4))
                # for a in dir(e):
                #     if not a.startswith('_'):
                #         print(a + ':\t', getattr(e, a))
            print('--------------------------------------------------------')


# stream = posts + gh_events


