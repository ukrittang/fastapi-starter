import sentry_sdk
from fastapi import FastAPI
from sentry_asgi import SentryMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request

from app.api.api_v1.api import api_router
from app.core import config
from app.db.session import Session

if config.DEBUG:
    app = FastAPI()
else:
    app = FastAPI(docs_url=None, redoc_url=None)

sentry_sdk.init(dsn=config.SENTRY_DSN)

# CORS
origins = []

# Set all CORS enabled origins
if config.BACKEND_CORS_ORIGINS:
    origins_raw = config.BACKEND_CORS_ORIGINS.split(",")
    for origin in origins_raw:
        use_origin = origin.strip()
        origins.append(use_origin)
    # pylint: disable=expression-not-assigned
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    ),

app.add_middleware(SentryMiddleware)
app.include_router(api_router, prefix=config.API_V1_STR)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = Session()
    response = await call_next(request)
    request.state.db.close()
    return response
