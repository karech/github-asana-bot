import logging

import sentry_sdk
from github_webhooks import create_app
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from . import handlers
from .settings import settings

app = create_app(secret_token=settings.GITHUB_WEBHOOKS_TOKEN)


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
