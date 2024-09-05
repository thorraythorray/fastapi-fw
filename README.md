# fastapi-FW

#### Launcher
```
uvicorn asgi:app --reload
```

#### Migrations

```
# init config
aerich init -t app.TORTOISE_ORM

# init db (不利于迁移，执行后最好把所有的app models在同时执行一次，有利于后面去迁移)
aerich init-db

# 每个app都要初始化db
aerich --app auth init-db

# 生成sql
aerich --app auth migrate

# 执行sql
aerich --app auth upgrade
```