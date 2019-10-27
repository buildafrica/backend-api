# Missing Persons Archive Backend [![Build Status](https://travis-ci.com/dcmpa/backend.svg?branch=master)](https://travis-ci.com/dcmpa/backend)

### Prerequisites

- python 3 (as `python`, else replace all example `python` commands with `python3`)
- postgres

# Project Setup 

- Make a directory on your computer for this project to live in:
  `mkdir wecodeafrica`
- Change to that directory:
  `cd wecodeafrica`
- Clone this repo
  `git clone https://github.com/wecodeafrica/backend`
- Alternately, you can fork this repo and then clone your fork.
- Change to the backend directory you just cloned: 
  `cd backend`
- Create a directory for your static files (normally it will be ignored by git)
  `mkdir backend/staticfiles`
    
## Set up a virtual environment with a python3.6 interpreter(Ubuntu):
```
virtualenv --python={PATH_TO_PYTHON3.6} dcmpa
source dcmpa/bin/activate
```

## Install requirements:
```
pip install -r requirements.txt
```
#### OSX Users:
If you get an error, you may need to open the `requiremnts.txt` file and replace `psycopg2==2.8.2` with `psycopg2-binary==2.8.3`


## Create your Postgres Database :
- Create a postgres databse by typing
  `createdb Dcmpa`
  When you are ready to exit Postgres, type ` \q` and then Enter

- Create a new user, you can do by by typing
  `createuser postgres --interactive --pwprompt`
  after which you will be prompted to create a new user.

## Set up environment variables:
- Copy the example .env file:
  `cp .env.example .env`

- Open the .env file and provide values for every variable with the value of `changeme`.
  `nano .env`
  
- Use the username, user password, and database name, for the postgres database you just created in the variables `POSTGRES_DB_NAME`, `POSTGRES_DB_USER`, and `POSTGRES_USER_PASSWORD`
    - (change the variables)
    - (save the .env file)

- Set the environmental variables
  `set -a && source .env && set +a`

## Prepare Your New Postgres Database :

- Make a migrations file to change your new database schema:
  `python manage.py makemigrations`

- Make a migrations file to change your new database schema:
  `python manage.py migrate`

- Make yourself a super user:
  `python manage.py createsuperuser`

  - You will be prompted by Django to create a super user, and you can use these credentials to log into the admin interface (more in next step)
  

## Start django:
- collect static, so you can run the django admin. You will run this command when you add or update static files:
  `python manage.py collectstatic`

- Run the server
  `python manage.py runserver`

- Navigate to the django admin:
  `http://localhost:8000/admin/`
  If you see a login screen, everything worked!


## Deployment
- master branch:- staging branch
- production branch:- production branch; the branch is tagged on each merge to show backend versioning.