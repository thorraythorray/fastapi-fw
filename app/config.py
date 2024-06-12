import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def init_environment():
    from dotenv import load_dotenv
    load_dotenv()
    return {k: v for k, v in dict(os.environ).items()}


ENVIRON = init_environment()

ALLOW_ORIGINS = [
    "http://localhost",
    "http://localhost:8080",
]

DATABASE_DB_URL = 'mysql://{}:{}@{}:{}/{}'.format(
    ENVIRON["MYSQL_HOST"],
    ENVIRON["MYSQL_PORT"],
    ENVIRON["MYSQL_USER"],
    ENVIRON["MYSQL_PASSWD"],
    ENVIRON["MYSQL_DB"],
)
