# Limbook Api
[![Actions Status](https://github.com/limvus/limbook-api/workflows/Build%20And%20Test/badge.svg)](https://github.com/limvus/limbook-api/actions)

Limbook api is a minimal REST Api for creating social app like facebook or twitter. 
It has basic features like posts, comments and react.

**Motivation**

I had met quite a few people who have wanted to have their own private social network
for their office or fun project. So, to help them, I had create this minimal version 
of the social API which they can integrate easily into their design and have the
app up and running in no time. Also, they can take this as a starter and build
on top of this api.

**Technology Used**
- Python
- Flask
- Flask-SQlalchemy
- Redis
- Redis Queue
- Postgresql
- Auth0

All python code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/) 

**For documentation of API visit here:**
 
**[API DOCUMENTATION](https://documenter.getpostman.com/view/3230491/SzmmVueg)**

## Features
- Post
- Comment
- React
- Image Manager

**Upcoming Features**
- Chat
- Notification
- Activity
- User Bot

## System Requirements
- Python >= 3.7
- Pip >= 19.0
- redis-server

Note: may run in lower version but haven't tested.

## Installation
Using virtual environment
```shell script
# go to project directory and create venv
$ virtualenv venv
$ (or) python3 -m venv path_to_project/venv
# source venv from project directory
$ source venv/bin/activate
```
Install dependencies
```shell script
$ pip install -r requirements.txt
```
Export secrets
```shell script
# in ~/.profile add your env variables:
export SECRET_KEY='my_secret_key' #any random string
export DATABASE_URL= #db path
export REDIS_URL= # redis url
export MAIL_SERVER= # mail server host
export MAIL_PORT= # mail server port
export MAIL_USERNAME= # mail username
export MAIL_PASSWORD= # mail password
export DEMO_USER_PASSWORD= # password for demo seed user
# logout and login or
$ source ~/.profile
```
Run migration
```shell script
# initialize and run migration
flask db init
flask db migrate
flask db upgrade
```
Seed demo data
```shell script
flask seed run
# Security Note: seed data has some default users with password.
# admin@gmail.com/password
# verified_user@gmail.com/password
# unverified_user@gmail.com/password
```
Run Redis Server and Worker
```shell script
# if you want to use redis queue you need to enable redis server and worker
# to run redis-server
redis-server

# to run worker
python worker.py

# or you can disable redis in the config: 
USE_REDIS=False
```
Run app
```shell script
# using python
python run.py
# using flask
export FLASK_APP=limbook_api
flask run
```
This should bring the api up and running at:

http://localhost:5000

## Test
```shell script
# Note: unittest may not detect all the tests. So use PYTEST:
# Simply run pytest from the root directory.
pytest
```

Debugging with python interpreter
```
# in the command line
python

# inside python interpreter set app context
from run import app

# now you can test and try
from limbook_api.setup_db import db
from limbook_api.models import Post
post = Post(user_id="id",content="my post")
db.session.add(post)
```

## Deployment: Heroku
- Create new app in heroku
- Add Postgresql and Redis as addons
- Connect github to the app
- Set config vars (secret_key, db url, mail credentials etc)
- Create pipeline and add app to the pipeline
- Choose auto-deploy master branch
- Make sure both web and worker dyno are running:  
    heroku ps:scale web=1 worker=1

## Contribution
If you want to contribute, just fork the repository and play around, create 
issues and submit the pull request. Help is always welcomed.

## Security
If you discover any security related issues, please email hello@sudiplimbu.com 
instead of using the issue tracker.

## License
The scripts and documentation in this project are released under the MIT License

## Author
Sudip Limbu