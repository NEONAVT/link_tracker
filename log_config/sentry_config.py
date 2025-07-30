import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from sentry_sdk.integrations.redis import RedisIntegration
from settings import settings


def setup_sentry(app):
    """
    Инициализирует Sentry SDK и оборачивает ASGI-приложение.

    Если в настройках задан SENTRY_DSN, настраивает интеграцию с Redis,
    устанавливает sample rate и окружение. Возвращает обёртку
    SentryAsgiMiddleware над приложением. Иначе возвращает оригинальное
    приложение без изменений.

    Args:
        app: ASGI-приложение.

    Returns:
        Обёрнутое или исходное ASGI-приложение.
    """
    if settings.SENTRY_DSN:
        sentry_sdk.init(
            dsn=settings.SENTRY_DSN,
            integrations=[RedisIntegration()],
            traces_sample_rate=1.0,
            environment=settings.ENVIRONMENT
        )
        return SentryAsgiMiddleware(app)
    return app
