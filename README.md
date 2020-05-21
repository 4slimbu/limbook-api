# Limbook Api
![](https://github.com/limvus/limbook-api/workflows/limbook-api-ci/badge.svg)

Limbook api is a minimal api for creating social app like facebook or twitter. 
It has basic features like user, role and permission management plus support 
for posts, comments, react and friends. It is currently at version 1.0. More 
features will be added in the next release, so keep checking for updates.

** For documentation of API visit here: **
 
**[API DOCUMENTATION](https://documenter.getpostman.com/view/3230491/SzmmVueg)**

## Features


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
# in ~/.profile add your env variables. e.g:
export SECRET_KEY='my_secret_key' #any random string
export SQLALCHEMY_DATABASE_URI='sqlite:///site.db' #db path
# logout and login or
$ source ~/.profile
```
Run app
```shell script
# using python
python run.py
# using flask
export FLASK_APP=limbook_api
flask run
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
```

## Test
```shell script
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

## Contribution
If you want to contribute, just fork the repository and play around, create 
issues and submit pull request. Help is always welcomed.

## Security
If you discover any security related issues, please email hello@sudiplimbu.com 
instead of using the issue tracker.

## Author
Sudip Limbu