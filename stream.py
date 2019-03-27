#!/usr/bin/env python3
from app.models import *
from app.views import gh_stream


all_event_types = [
    'CheckRunEvent',                        # irrelevent
    'CheckSuiteEvent',                      # irrelevent
    'CommitCommentEvent',       
    'ContentReferenceEvent',                # irrelevent
    'CreateEvent',
    'DeleteEvent',                          # not needed
    'DeploymentEvent',                      # not visible in timeline
    'DeploymentStatusEvent',                # not visible in timeline
    'DownloadEvent',                        # no longer delivered
    'FollowEvent',                          # no longer delivered
    'ForkEvent',
    'ForkApplyEvent',                       # no longer delivered
    'GitHubAppAuthorizationEvent',          # irrellevent
    'GistEvent',                            # no longer delivered
    'GollumEvent',                          # irrelevent
    'InstallationEvent',                    # irrelevent
    'InstallationRepositoriesEvent',        # irrelevent
    'IssueCommentEvent',
    'IssuesEvent',
    'LabelEvent',                           # not visible in timeline
    'MarketplacePurchaseEvent',             # irrelevent
    'MemberEvent',
    'MembershipEvent',                      # not visible in timeline
    'MilestoneEvent',                       # not visible in timeline
    'OrganizationEvent',                    # not visible in timeline
    'OrgBlockEvent',                        # not visible in timeline
    'PageBuildEvent',                       # not visible in timeline
    'ProjectCardEvent',
    'ProjectColumnEvent',
    'ProjectEvent',
    'PublicEvent',
    'PullRequestEvent',
    'PullRequestReviewEvent',
    'PullRequestReviewCommentEvent',
    'PushEvent',
    'ReleaseEvent',
    'RepositoryEvent',                     # not visible in timeline
    'RepositoryImportEvent',               # irellevent
    'RepositoryVulnerabilityAlertEvent',   # irrelevent
    'SecurityAdvisoryEvent',               # irrelevent
    'StatusEvent',                         # not visible in timeline
    'TeamEvent',                           # not visible in timeline
    'TeamAddEvent',                        # not visible in timeline
    'WatchEvent'
]

handled_event_types = [
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

def putPost(post):
    print("title:", post.title)
    print("published:", post.published)
    print("content")
    print(post.content)
    print('----------------------------------------')

user = Author.objects.get(username='githuber')

posts = []
posts = list(Post.objects.all())
# for post in posts:
#     putPost(post)

gh_activity = gh_stream.get_activities(user, 10)
# print('len activity:', len(gh_activity))

stream = posts + gh_activity
stream.sort(key=lambda post: post.published, reverse=True)
for post in stream:
    putPost(post)


