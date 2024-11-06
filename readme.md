# create virtual env and activate

## py -m venv env
## .\env\Scripts\activate

# Install all the requirements

## pip install -r requirements.txt

# Now Run Python Server

## python manage.py runserver 0.0.0.0:8006


# DOCKER

## docker build --tag python-django .
## docker run --publish 8006:8006 python-django
