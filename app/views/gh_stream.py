#!/usr/bin/env python3
from app.models import *
from urllib.parse import urlparse
from datetime import datetime
from datetime import date
from pytz import utc
import github
import sys


EVENT_TYPES = [
    'CommitCommentEvent',
    'CreateEvent',
    'ForkEvent',
    'IssueCommentEvent',
    'IssuesEvent',
    'MemberEvent',
    'ProjectCardEvent',
    'ProjectColumnEvent',
    'ProjectEvent',
    'PublicEvent',
    'PullRequestEvent',
    'PullRequestReviewEvent',
    'PullRequestReviewCommentEvent',
    'PushEvent',
    'ReleaseEvent',
    'WatchEvent'
]

def get_activities(author, max_page_number):
    # get github events for user
    parse_result = urlparse(author.github_url)
    gh_username = parse_result.path.lstrip('/')
    events = github.Github().get_user(gh_username).get_events()

    # get last year's date
    today = date.today()
    last_year_today = datetime(today.year - 1, today.month, today.day)

    gh_activities = []
    for i in range(max_page_number):
        try:
            page = events.get_page(page=i)
            if page:
                for e in page:
                    if e.created_at >= last_year_today:
                        new_post = event2post(e, author)
                        gh_activities.append(new_post)
            else:
                # no more results
                break
        except Exception as exc:
            # exc_type, exc_obj, tb = sys.exc_info()
            # print("!!!!EXCEPTION!!!!")
            # print('exception', exc)
            # print('lineno', tb.tb_lineno)
            break
    return gh_activities

def event2post(e, user):
    title = ''
    description = ''
    content = ''
    if e.public:
        visibility = 'PUBLIC'
    else:
        visibility = 'PRIVATE'

    # date formats
    current_tz = datetime.now().astimezone().tzinfo
    dt_utc = utc.localize(e.created_at)
    # dt_str = dt_local.strftime('%a %b %d %H:%M:%S %Y %z')

    if e.type == 'CommitCommentEvent':
        title = 'Github commit'
        description = 'github_CommitCommentEvent'
        if e.actor.name:
            author = e.actor.name
        else:
            author = e.actor.login
        content = (
            'commit %s' % e.payload['comment']['commit_id'] +
            'Repository: %s\n' % e.repo.name +
            'Author %s\n' % author +
            '\n\t %s\n' % e.payload['comment']['body']
        )

    elif e.type == 'CreateEvent':
        title = 'Github ' + e.payload['ref_type'] + ' created'
        description = 'github_CreateEvent'
        content = 'Created ' + e.payload['ref_type'] + ' '
        if e.payload['ref_type'] == 'repository':
            content += 'repository ' + e.repo.name
        elif e.payload['ref_type'] == 'branch':
            content += e.payload['ref'] + ' on repository ' + e.repo.name
        content += 'repo url: %s\n' % e.repo.html_url
        if e.payload['description']:
            content += '\n' + e.payload['description'] + '\n'

    elif e.type == 'ForkEvent':
        title = 'Github repository forked'
        description = 'github_ForkEvent'
        content = (
            'forked %s\n' % e.payload['forkee']['full_name'] +
            'from %s(https://github.com/%s)\n' % (e.repo.name, e.repo.name)
        )

    elif e.type == 'IssueCommentEvent':
        title = 'Github issue comment %s' % e.payload['action']
        content = (
            'A comment was %s for issue \'%s\' ' %
            (e.payload['action'], e.payload['issue']['title']) +
            'on repository %s \n' % e.repo.name +
            e.payload['comment']['body']
        )

    elif e.type == 'IssuesEvent':
        title = 'Github Issue %s' % e.payload['action']
        description = 'github_IssuesEvent'
        content = (
            'issue #%d: %s\n' %
            (e.payload['issue']['number'], e.payload['issue']['title']) +
            'Author: %s\n' % e.payload['issue']['user']['login'] +
            'Labels:'
        )
        for label in e.payload['issue']['labels']:
            content += ' ' + label['name']

        if e.payload['issue']['assignees']:
            content += '\nAssignees:'
            for assignee in e.payload['issue']['assignees']:
                content += ' ' + assignee

        content += '\n' + e.payload['issue']['body']


    elif e.type == 'MemberEvent':
        title = 'Github a collaborator on repository %s has been %s' % (
            e.repo.name, e.payload['action'])
        description = 'github_MemberEvent'
        if e.payload['action'] == ('added', 'deleted'):
            content = (
                '%s has been %s as a collaborator ' %
                (e.payload['member']['login'], e.payload['action'])
            )
        else:
            content = (
                '%s\'s permission has been %s' %
                (e.playload['member']['login'], e.payload['action'])
            )

    elif e.type == 'PublicEvent':
        title = 'Github repository %s has been made public'
        description = 'github_ForkEvent'
        content = 'Github repository %s has been made public\n' % e.repo.name


    elif e.type == 'PullRequestEvent':
        title = 'Github a pull request was %s' % e.payload['action']
        description = 'github_PullRequestEvent'
        content = (
            'pull request #%d: %s\n' %
            (e.payload['pull_request']['number'], e.payload['pull_request']['title']) +
            'was %s on repository %s by %s\n' %
            (e.payload['action'], e.repo.name, e.payload['pull_request']['user']['login']) +
            'State: %s\n' % e.payload['pull_request']['state'] +
            'URL: %s\n' % e.payload['pull_request']['html_url'] +
            e.payload['pull_request']['body']
        )

    elif e.type == 'PullRequestReviewEvent':
        title = 'Github pull request review is %s' % e.payload['action']
        description = 'github_PullRequestReviewEvent'
        dt_utc = utc.localize(e.payload['review']['submitted_at'])
        content = (
            'a review was %s for pull request #%d on repository %s\n by %s' %
            (e.payload['action'],
             e.payload['pull_request']['number'],
             e.repo.name,
             e.payload['review']['user']['login']) +
            'URL: %s\n' % e.payload['review']['html_url'] +
            e.payload['review']['body']
        )

    elif e.type == 'PushEvent':
        title = 'Github %s pushed to repository %s' % (e.actor.login, e.repo.name)
        description = 'github_PushEvent'
        content = '%d commit(s) was pushed to branch %s by %s' % (e.payload['size'], e.payload['ref'], e.actor.login)


    elif e.type == 'ReleaseEvent':
        title = 'Github a release was published'
        description = 'github_ReleaseEvent'
        dt_utc = utc.localize(e.payload['release']['published_at'])
        content = (
            'a release was published by %s on repository %s\n' %
            (e.payload['release']['author']['login'], e.repo.name) +
            'URL: %s\n' % e.payload['release']['html_url']
        )
        if e.payload['release']['name']:
            content += e.payload['release']['name'] + '\n'
        if e.payload['release']['body']:
            content += e.payload['release']['body']

    elif e.type == 'WatchEvent':
        title = 'Github a repo is starred'
        description = 'github_WatchEvent'
        content = 'repository %s was starred by %s\n' % (e.repo.name, e.actor.login)


    else:
        content = e.payload

    # return a post
    return Post(
        author      = user,
        published   = dt_utc,
        title       = title,
        description = description,
        visibility  = visibility,
        content     = content)

