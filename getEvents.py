#!/usr/bin/env python
import github
import pickle
import json
from datetime import datetime
from pytz import utc
from time import sleep

# gh_user = github.Github().get_user()
gh_user = github.Github().get_user()
events = gh_user.get_events()

enough = False
counts = 0
events_list = []
for i in range(200):
    try:
        print(i)
        page = events.get_page(i)
        if page:
            for e in page:
                if e.type == 'WatchEvent':
                    print(e)
                    events_list.append(e)
                    counts += 1
                if counts >= 5:
                    enough = True
                    break
            if enough:
                break
            # sleep(1)
        else:
            print('end of result')
            break
    except Exception as exc:
        print(exc)
        break
print(counts)
with open('gh_events.data', 'wb') as f:
    pickle.dump(events_list, f)

events_list = []
with open('gh_events.data', 'rb') as f:
    events_list = pickle.load(f)

for e in events_list:
    print(json.dumps(e.raw_data, indent=4))
    # title = 'Issue  %s' % e.payload['action']

    # # # date formatting
    # tz = datetime.now().astimezone().tzinfo
    # dt = utc.localize(e.created_at).astimezone(tz)
    # dt_str = dt.strftime('%a %b %d %H:%M:%S %Y %z')

    # content = (
    #     'A comment was %s for issue \'%s\' ' 
    #     % (e.payload['action'], e.payload['issue']['title']) + 
    #     'on repository %s \n' % e.repo.name +
    #     'Date: %s\n' % dt_str +
    #     e.payload['comment']['body']
    # )
    # print('title:', title)
    # # print('published:', e.created_at)
    # print('content:\n' + content)
    print('-----------------------------------------------')
