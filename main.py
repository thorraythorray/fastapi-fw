from app.initialize import init_fastapi_app, init_tortoise

app = init_fastapi_app()


@app.on_event("startup")
async def startup_event():
    await init_tortoise()
