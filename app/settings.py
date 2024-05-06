import os


def init_environment():
    from dotenv import load_dotenv

    load_dotenv()
    return {k: v for k, v in dict(os.environ).items()}


ENVIRON = init_environment()


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ALLOW_ORIGINS = [
    "http://localhost",
    "http://localhost:8080",
]

ALLOW_CREDENTIALS = True

ALLOW_METHODS = ["*"]

ALLOW_HEADERS = ["*"]


DATABASE_DB_URL = 'mysql://{}:{}@{}:{}/{}'.format(
    ENVIRON["MYSQL_HOST"],
    ENVIRON["MYSQL_PORT"],
    ENVIRON["MYSQL_USER"],
    ENVIRON["MYSQL_PASSWD"],
    ENVIRON["MYSQL_DB"],
)