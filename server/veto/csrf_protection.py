# See OWASP CSRF prevention information.

import secrets
from http import HTTPStatus
from urllib.parse import urlparse

from flask import current_app, g, render_template, request, session
from itsdangerous import BadData, URLSafeTimedSerializer

CSRF_SAFE_HTTP_METHODS = ["GET", "HEAD", "OPTIONS", "TRACE"]
CSRF_TOKEN_BYTE_LENGTH = 32
CSRF_TOKEN_HEADER_NAME = "CSRF-Token"
CSRF_TOKEN_MAX_AGE = 3600
CSRF_TOKEN_NAME = "csrf_token"


def generate_csrf_token():
    secret = current_app.config["SECRET_KEY"]
    serializer = URLSafeTimedSerializer(secret, salt=CSRF_TOKEN_NAME)
    return serializer.dumps(secrets.token_hex(CSRF_TOKEN_BYTE_LENGTH))


def set_csrf_token():
    token = generate_csrf_token()
    session[CSRF_TOKEN_NAME] = token
    setattr(g, CSRF_TOKEN_NAME, token)
    return token


def unset_csrf_token():
    session.pop(CSRF_TOKEN_NAME, None)
    g.pop(CSRF_TOKEN_NAME, None)


def reset_csrf_token():
    unset_csrf_token()
    return set_csrf_token()


def is_invalid_origin():
    request_origin = request.headers.get("origin", request.headers.get("referer"))

    if request_origin is None:
        # These headers are "forbidden" and can't normally be modified
        # programmatically in a browser. So, if they're missing, it's probably
        # for a good reason, and invalidating the request could cause usability
        # problems. However, since that has a low probability of happening, we
        # err on the side of being more secure.
        return True

    request_origin = urlparse(request_origin)
    target_origin = urlparse(current_app.config["CSRF_TARGET_ORIGIN"])

    invalid = any(
        [
            request_origin.scheme != target_origin.scheme,
            request_origin.hostname != target_origin.hostname,
            request_origin.port != target_origin.port,
        ]
    )

    return True if invalid else False


def is_invalid_csrf_token():
    # We assume that a CSRF token exists in a secured session (i.e.
    # SESSION_COOKIE_HTTPONLY = True, SESSION_COOKIE_SAMESITE = "Lax" or
    # "Strict", etc.), and that the same CSRF token is sent in a header. Form
    # data is not checked since the client is a single-page application.

    session_token_encoded = session.get(CSRF_TOKEN_NAME)
    header_token_encoded = request.headers.get(CSRF_TOKEN_HEADER_NAME)

    if not all([session_token_encoded, header_token_encoded]):
        return True

    serializer = URLSafeTimedSerializer(
        current_app.config["SECRET_KEY"], salt=CSRF_TOKEN_NAME
    )

    try:
        session_token = serializer.loads(
            session_token_encoded, max_age=CSRF_TOKEN_MAX_AGE
        )
        header_token = serializer.loads(
            header_token_encoded, max_age=CSRF_TOKEN_MAX_AGE
        )
    except BadData:
        return True

    return not secrets.compare_digest(session_token, header_token)


def protect_request_from_csrf():
    if request.method in CSRF_SAFE_HTTP_METHODS:
        return

    if any([is_invalid_origin(), is_invalid_csrf_token()]):
        unset_csrf_token()
        msg = "Your request to modify data could not be validated."
        code = HTTPStatus.FORBIDDEN.value

        if request.accept_mimetypes.accept_html:
            return render_template(f"errors/{code}.jinja", msg=msg), code
        else:
            return {"msg": msg, "error_info": "INVALID_CSRF_TOKEN"}, code
