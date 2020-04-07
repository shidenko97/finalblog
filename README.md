# Finalblog
[![CircleCI](https://circleci.com/gh/shidenko97/finalblog.svg)](https://circleci.com/gh/shidenko97/finalblog)

A simple blog with REST API based on [Flask web-framework](https://flask.palletsprojects.com/en/1.1.x/). Created as a final task for a [Python Advanced Course at ITEA](https://itea.ua/uk/courses_itea/python_programming/python_advanced/)

### Quick start
For a getting started you need to run following command:
```
docker-compose up
```
and application will be available on next address: http://127.0.0.1:5000/. 
Further you need to register new account on http://127.0.0.1:5000/auth/register page.
Congratulations, now you can use the blog and its API.

### API
The application has a REST API based on [Flask-RESTPlus](https://flask-restplus.readthedocs.io/en/stable/) extension.
Api module available on http://127.0.0.1:5000/api and includes next models:
- User
- Role
- Post
- Comment

**Important:** Using an API requires Basic authorization.

### Tests
The app runs various tests:
- unit tests for database models (using unittest).

For manually run tests execute following command: 
```
python -m unittest tests.py
```

**Note:** See the tests.py files in each module for details.

### Todo
The application will be finalized by [following todos](https://github.com/shidenko97/finalblog/projects/1)