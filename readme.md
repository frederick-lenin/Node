create virtual env and activate
cmd : py -m venv env
cmd : .\env\Scripts\activate

Install all the requirements
cmd : pip install -r requirements.txt

Now Run Python Server
cmd : python manage.py runserver 0.0.0.0:8006


DOCKER
cmd : docker build --tag python-django .
cmd : docker run --publish 8006:8006 python-django
