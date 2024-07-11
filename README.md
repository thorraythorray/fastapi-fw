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

# 每个app都要初始化db
aerich --app core init-db

# 生成sql
aerich --app core migrate

# 执行sql
aerich --app core upgrade
```