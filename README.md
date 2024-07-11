# fastapi-FW

#### Launcher
```
uvicorn asgi:app --reload
```

#### Migrations

```
# init config
aerich init -t app.TORTOISE_ORM

# init db
aerich init-db
# aerich --app core init-db
```