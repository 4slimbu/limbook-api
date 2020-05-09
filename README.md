# Limbook Api
A simple starter template for Flask Application

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