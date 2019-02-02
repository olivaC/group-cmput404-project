## Getting Started Locally

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python3
- Pip
- Virtualenv
- settings_server.py

### Setting up for the first time
1. **_Clone this repository_**
2. **_cd into the group-cmput404-project directory._**
3. **_Add the settings_server.py file here_**
```
group-cmput404-project/
├── SocialDistribution/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── app/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│── manage.py
│   └── wsgi.py
└── settings_server.py
```
5. **_Create a Virtual Environment using python3 and activate it._**

6. **_Install requirements.txt_**
```
$ pip install -r requirements.txt
```

7. **_Test localhost to see if installation worked._**
```
$ python manage.py runserver
```