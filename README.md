# Limbook Api
An api for social network.

**Under development. Please check back later.**

**First release is scheduled for: May 16 2020**

**Feel free to contribute**

# Installation
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
# in .bash_profile add these lines
export SECRET_KEY='my_secret_key' #any random string
export SQLALCHEMY_DATABASE_URI='sqlite:///site.db' #db path
# source .bash_profile
$ source ~/.bash_profile
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

# Test
```shell script
python -m unittest tests/app_test.py
```

# Debugging with python interpreter
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