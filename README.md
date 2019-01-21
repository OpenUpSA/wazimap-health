[Sexual and Reproductive Health Activities Map](http://activities4srh.org.za/)
===============================================================================

The South African youth and health centered instance of [Wazimap](https://github.com/Code4SA/wazimap)

# Local Development

1. clone the repo
2. ``cd wazimap_health``
3. ``virtualenv --no-site-packages env``
4. ``source env/bin/activate``
5. ``pip install -r requirements.txt``

You will need a Postgres database for the instance you are running, and type the following commands

```
$ su postgres

$ createuser wazimap_health -P

$ createdb -O wazimap_health wazimap_health

$ psql

$ add the extension hstore on the wazimap_health database
```

Import the data into the new database.

Some of the tables are not managed by django directly, so we have to manaually create them.

```
cat sql/*.sql | psql -U wazimap_health -W wazimap_health
```

Run migrations to keep Django happy:

```
python manage.py migrate
```

Import the fixtures for the django models:

```
python manage.py loaddata fixtures/health.json
python manage.py loaddata fixtures/wazimap.json
```

Create an admin user:

```
python manage.py createsuperuser

```

Start the server:

```
python manage.py runserver
```
