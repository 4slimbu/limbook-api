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
python run.py
```