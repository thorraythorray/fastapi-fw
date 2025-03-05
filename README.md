## fastapi-admin

#### Launcher
```
uvicorn asgi:app --host 0.0.0.0 --port 8000 --reload
```

#### Migrations
```
# init config
aerich init -t app.config.TORTOISE_ORM

# initialize
python manage.py db init

# makemigrations
python manage.py db migrate --app <app_name> --name <change_name>

# sync db 升级
python manage.py db upgrade --app <app_name>

# sync db 降级
python manage.py db downpgrade --app <app_name>
```

#### Lint
```
python manage.py lint
```