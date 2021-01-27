import os
from datetime import datetime

import click
from dateutil.tz import tzlocal


def setup_sentry():
    if os.getenv("SENTRY_ENABLED") == "yes":
        now = datetime.now(tzlocal()).strftime("%Y-%m-%d %H:%M:%S %z")
        click.echo(f"[{now}] Enabling Sentry to track errors")
        import sentry_sdk
        from sentry_sdk.integrations.flask import FlaskIntegration

        sentry_sdk.init(
            dsn=os.getenv("SENTRY_DSN"),
            integrations=[FlaskIntegration()],
            traces_sample_rate=float(
                os.getenv("SENTRY_TRACES_SAMPLE_RATE", default=0.0)
            ),
        )
