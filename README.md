# Equipo

Django project to manage a team of freelancers. 

The project is being developed according the [12 factor app principles](https://12factor.net/).

The base skeleton has been setup with [Docker Django Boilerplate](https://github.com/lukin0110/docker-django-boilerplate).

## Usage

Init project:
```
$ docker-compose build
```

Setup database:
```
$ docker-compose up -d postgres
$ docker-compose run app setup_db
```

Launch:
```
$ docker-compose up app
```

Launch Nginx:
```
$ docker-compose up web
```

*Now your django app is available on http://localhost*

## Container commands

The image has 

Run a command:
```
$ docker-compose run app <command>
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
| uwsgi     | Run uwsgi server                                                                 |
| help      | Show this message                                                               |

### Create a Django app

```
$ docker-compose run app manage startapp myapp
```

### Create a super user
```
$ docker-compose run app manage createsuperuser
```
