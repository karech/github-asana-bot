import logging

import sentry_sdk
from github_webhooks import create_app
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from . import handlers
from .settings import settings

app = create_app(
    secret_token=settings.GITHUB_WEBHOOKS_TOKEN,
    debug=settings.DEBUG,
    openapi_url='/openapi.json' if settings.DEBUG else None,
    docs_url='/docs' if settings.DEBUG else None,
    redoc_url='/redoc' if settings.DEBUG else None,
    swagger_ui_oauth2_redirect_url='/docs/oauth2-redirect' if settings.DEBUG else None,
)


if settings.SENTRY_DSN:
    sentry_sdk.init(
        settings.SENTRY_DSN,
        sample_rate=0,
    )
    app.add_middleware(SentryAsgiMiddleware)


if settings.DEBUG:
    logging.getLogger().setLevel(logging.DEBUG)


app.hooks.add_handler('pull_request', handlers.PullRequestPayload, handlers.handle_pull_request)
app.hooks.add_handler('push', handlers.PushPayload, handlers.handle_push)
