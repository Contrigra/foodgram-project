# Foodgram.Cloud

## Website URL

http://www.foodgram.cloud/

## Docker Compose:
docker-compose up --build

## First Time Start

**For proper functionality** get inside the container and follow the next steps:

~~~
docker exec web -t -i <WEB CONTAINER ID> bash
~~~

**Make initial Django migrations:**
~~~
python manage.py migrate
~~~

**Populate initial tags** since base recipe filtering depends on it:
~~~
python manage.py create_tags
~~~

**Optionally** you can load my own ingredient data:
~~~
python manage.py load_ingredient_data
~~~
Ingredients are stored in ingredients.csv in the api management's folder


**Create superuser:**

~~~
python manage.py createsuperuser
~~~

## Used Tech Stack
Python 3.8

Django 3.14

PostgreSQL

Docker

django-taggit

unicode-slugify
