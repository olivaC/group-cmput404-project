# CMPUT 404 Project

[![Build Status](https://travis-ci.com/olivaC/group-cmput404-project.svg?branch=master)](https://travis-ci.com/olivaC/group-cmput404-project)

## Link to Group 10 Social Distribution

https://young-plains-33934.herokuapp.com

## Contributors
```
Musaed Alsobaie  
Carrol Jirakul  
Alex Li  
Carlo Oliva  
Weichen Wang  
```

## Webservice API Documentation
[Link to the API Documentation](https://github.com/olivaC/group-cmput404-project/wiki/Web-Service-API-&-Documentation)

## Working in this repository
When working on a new feature or issue please follow the following steps.

1. Create an issue on the issue tracker.
2. Take note of the issue #.
3. Create a branch starting with the issue number and then a descriptive title:

    ```
    git checkout -b 1-first-branch
    ```
4. When pushing your commits to your branch start with a "#{issue #} ...". This will help keep track of your commits to a specific issue.
    ```
    git commit -m "#1 First commit to this branch"
    ```
5. When finished, make a pull request with details on what you finished and how to test it. Add all group members as a reviewer and must receive at least 2 approvals to merge your code into the development branch.
6. Once your branch has been approved, go ahead and merge it into the development branch.

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
