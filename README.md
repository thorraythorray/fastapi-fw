## fastapi-admin

#### Launcher
```
uvicorn asgi:app --reload
```

#### Migrations
```
# initialize
python manage.py db init

# makemigrations
python manage.py db migrate --app <app_name> --name <change_name>

# sync db
python manage.py db upgrade
```