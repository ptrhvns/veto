from .veto.app_factory import create_app
from .veto.sentry import setup_sentry

# Call setup_sentry() as early as possible.
setup_sentry()

app = create_app()
