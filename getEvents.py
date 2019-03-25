#!/usr/bin/env python
import github
import pickle

gh_user = github.Github().get_user("skywolff")
events = gh_user.get_events()

events_list = []
for i in range(10):
    page = events.get_page(i)
    if page:
        for e in page:
            events_list.append(e)
    else:
        break

with open('gh_events.data', 'wb') as f:
    pickle.dump(events_list, f)

