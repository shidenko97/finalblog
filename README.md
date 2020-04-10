# Finalblog
[![CircleCI](https://circleci.com/gh/shidenko97/finalblog.svg)](https://circleci.com/gh/shidenko97/finalblog)

[Demo](https://flask-finalblog.herokuapp.com)

A simple blog with chat based on [AIOHTTP](https://docs.aiohttp.org/) and REST API based on [Flask web-framework](https://flask.palletsprojects.com/en/1.1.x/). Created as a final task for a [Python Advanced Course at ITEA](https://itea.ua/uk/courses_itea/python_programming/python_advanced/)

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

### Chat
Application has a chat based on websocket and implemented by [AIOHTTP](https://docs.aiohttp.org/).
The chat located in `/chat` directory and can be runned by following command:
```
python chat/main.py
```
and chat's websockets will be available on http://127.0.0.1:8080 url.

### Tests
The app runs various tests:
- unit tests for database models (using unittest).
- pytest tests for chat.

For manually run tests execute following command: 
```
python -m pytest tests.py
```

**Note:** See the tests.py files in each module and /tests directory for details.

### Todo
The application will be finalized by [following todos](https://github.com/shidenko97/finalblog/projects/1)