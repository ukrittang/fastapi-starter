from decouple import config

DEBUG = config("DEBUG")

API_V1_STR = "/api/v1"
API_AUTH_PREFIX = "/auth"
API_LOGIN_ROUTER = "/access-token"
API_LOGIN_URL = f"{API_V1_STR}{API_AUTH_PREFIX}{API_LOGIN_ROUTER}"

POSTGRES_SERVER = config("POSTGRES_SERVER")
POSTGRES_USER = config("POSTGRES_USER")
POSTGRES_PASSWORD = config("POSTGRES_PASSWORD")
POSTGRES_DB = config("POSTGRES_DB")
if POSTGRES_PASSWORD:
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}/{POSTGRES_DB}"
    )
else:
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{POSTGRES_USER}@{POSTGRES_SERVER}/{POSTGRES_DB}"
    )

REDIS_PASSWORD = config("REDIS_PASSWORD")
if REDIS_PASSWORD:
    REDIS_URI = f"redis://:{REDIS_PASSWORD}@localhost:6379/0"
else:
    REDIS_URI = "redis://localhost:6379/0"

SECRET_KEY = config("SECRET_KEY")

# 60 minutes * 24 hours * 8 days = 8 days
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 8

SERVER_NAME = config("SERVER_NAME")
SERVER_HOST = config("SERVER_HOST")
# # a string of origins separated by commas, e.g: "http://localhost, http://localhost:4200, http://localhost:3000, http://localhost:8080, http://local.dockertoolbox.tiangolo.com"
# BACKEND_CORS_ORIGINS = "http://localhost:8000, http://local.dockertoolbox.tiangolo.com"
BACKEND_CORS_ORIGINS = "http://localhost:3000"
PROJECT_NAME = config("PROJECT_NAME")
SENTRY_DSN = config("SENTRY_DSN")

SMTP_TLS = True
SMTP_PORT = 587
SMTP_HOST = config("SMTP_HOST")
SMTP_USER = config("SMTP_USER")
SMTP_PASSWORD = config("SMTP_PASSWORD")
EMAILS_FROM_EMAIL = config('EMAILS_FROM_EMAIL')
EMAILS_FROM_NAME = PROJECT_NAME
EMAIL_RESET_TOKEN_EXPIRE_HOURS = 48
EMAIL_TEMPLATES_DIR = "app/email-templates/build"
EMAILS_ENABLED = SMTP_HOST and SMTP_PORT and EMAILS_FROM_EMAIL

FIRST_SUPERUSER = "ukrit.tang@gmail.com"
FIRST_SUPERUSER_PASSWORD = "your_password"
