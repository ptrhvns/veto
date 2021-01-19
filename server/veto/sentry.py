import os


def setup_sentry():
    if os.getenv("SENTRY_ENABLED") == "yes":
        import sentry_sdk
        from sentry_sdk.integrations.flask import FlaskIntegration

        sentry_sdk.init(
            dsn=os.getenv("SENTRY_DSN"),
            integrations=[FlaskIntegration()],
            traces_sample_rate=float(
                os.getenv("SENTRY_TRACES_SAMPLE_RATE", default=0.0)
            ),
        )
