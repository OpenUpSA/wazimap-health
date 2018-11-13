Wazimap Health
====================

The South African youth and health centered instance of [Wazimap](https://github.com/Code4SA/wazimap)

# Local Development

1. clone the repo
2. ``cd wazimap_health``
3. ``virtualenv --no-site-packages env``
4. ``source env/bin/activate``
5. ``pip install -r requirements.txt``

You will need a Postgres database for the instance you are running:

```
psql

create user wazimap_health with password wazimap_health

create database wazimap_health

grant all privileges on database wazimap_health to wazimap_health

```

Import the data into the new database.

```
cat sql/*.sql | psql -U wazimap_health -W wazimap_health
```

Run migrations to keep Django happy:

```
python manage.py migrate
```

Import the fixtures for the django models:

```
python manage.py loaddata fixtures/wazimap_health/wazimap_django_models.json
```

Create an admin user:

```
python manage.py createsuperuser

```

Start the server:

```
python manage.py runserver
```
