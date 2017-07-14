# Docker Django Boilerplate

Minimal setup for a Django project with Docker, following 
[the 12factor app](https://12factor.net/) principles. This repo contains 
skeleton code to get up and running with Docker & Django quickly. The 
image uses [uWSGI](https://uwsgi-docs.readthedocs.io/) to host the 
Django project. It's up to you to put Nginx or Apache in front in 
production.  

This image is **not intended** as being a base image for a Django project.
It's a boilerplate, you can copy/paste this and use it as a base to 
start a project. The image contains the *hello* Django project. 
[Replace the word *hello* with the name of *your project*](docs/rename.md).

## Usage

Download the repository:
```
$ git clone https://github.com/lukin0110/docker-django-boilerplate.git
```

Init project:
```
$ cd docker-django-boilerplate
$ docker-compose build

For Windows:
$ cd docker-django-boilerplate
$ docker-compose -f 'docker-compose-windows' build
```

Setup database:
```
$ docker-compose up -d postgres
$ docker-compose run app setup_db

Docker can't setup postgres db on Windows. Install postgres from the website.
https://www.postgresql.org/download/windows/

add '.env' file to the root with following settings:
POSTGRES_DB_NAME=*database name*
POSTGRES_PORT_5432_TCP_ADDR=*ip adress*
POSTGRES_PORT_5432_TCP_PORT=5432
POSTGRES_USER=*postgres user who has access to the db*
POSTGRES_PASSWORD=*password of the user*
```

Launch:
```
$ docker-compose up app

For Windows:
$ docker-compose -f 'docker-compose-windows' up app
```

Launch Nginx *(optional)*:
```
$ docker-compose up web
```

*Now your django app is available on http://localhost, but it's optional for development*

## Container commands

The image has 

Run a command:
```
$ docker-compose run app <command>

For Windows:
$ docker-compose -f 'docker-compose-windows' run app <command>
```

Available commands:

| Command   | Description                                                                     |
|-----------|---------------------------------------------------------------------------------|
| dev       | Start a normal Django development server                                        |
| bash      | Start a bash shell                                                              |
| manage    | Start manage.py                                                                 |
| setup_db  | Setup the initial database. Configure *$POSTGRES_DB_NAME* in docker-compose.yml |
| lint      | Run pylint                                                                      |
| python    | Run a python command                                                            |
| shell     | Start a Django Python shell                                                     |
| uwsgi     | Run uwsgi server                                                                |
| help      | Show this message                                                               |

### Create a Django app

```
$ docker-compose run app manage startapp myapp

For Windows:
$ docker-compose -f 'docker-compose-windows' run app manage startapp myapp
```

### Create a super user
```
$ docker-compose run app manage createsuperuser

For Windows:
$ docker-compose -f 'docker-compose-windows' run app manage createsuperuser
```

### Create fixtures
```
$ docker-compose run app manage dumpdata <appname> --format=json --indent=4 > <filename.json>

For Windows:
$ docker-compose -f docker-compose-windows.yml run app manage dumpdata <appname> --format=json --indent=4 > <filename.json>

After creating the fixtures make sure they are encoded in the utf-8 format (no DOM). You can view/edit the format with notepad++.
```

### Save permissions in a fixture
```
https://docs.djangoproject.com/en/dev/topics/serialization/#natural-keys

$ docker-compose run app manage dumpdata auth --format=json --indent=4 --natural-foreign --natural-primary -e auth.Permission > <filename.json>

For Windows:
$ docker-compose -f docker-compose-windows.yml run app manage dumpdata auth --format=json --indent=4 --natural-foreign --natural-primary -e auth.Permission > <filename.json>
```

### Load fixtures
```
https://docs.djangoproject.com/en/1.11/ref/django-admin/#loaddata

$ docker-compose run app manage loaddata

For Windows:
$ docker-compose -f docker-compose-windows.yml run app manage loaddata
```

## Awesome resources

Useful awesome list to learn more about all the different components used in this repository.

* [Docker](https://github.com/veggiemonk/awesome-docker)
* [Django](https://gitlab.com/rosarior/awesome-django)
* [Python](https://github.com/vinta/awesome-python)
* [Nginx](https://github.com/agile6v/awesome-nginx)
* [AWS](https://github.com/donnemartin/awesome-aws)

## Useful links

* [Docker Hub Python](https://hub.docker.com/_/python/)
* [Docker Hub Postgres](https://hub.docker.com/_/postgres/)
* [Docker compose Postgres environment variables](http://stackoverflow.com/questions/29580798/docker-compose-environment-variables)
* [Quickstart: Docker Compose and Django](https://docs.docker.com/compose/django/)
* [Best practices for writing Dockerfiles](https://docs.docker.com/engine/userguide/eng-image/dockerfile_best-practices/)

