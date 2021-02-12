import secrets
from http import HTTPStatus

from flask import g, session
from itsdangerous import URLSafeTimedSerializer
from veto.csrf_protection import (
    CSRF_SAFE_HTTP_METHODS,
    CSRF_TOKEN_MAX_AGE,
    CSRF_TOKEN_NAME,
    generate_csrf_token,
    is_invalid_csrf_token,
    is_invalid_origin,
    protect_request_from_csrf,
    reset_csrf_token,
    set_csrf_token,
    unset_csrf_token,
)


def test_generate_csrf_token(app_fn, monkeypatch):
    actual_token = "abcde12345"
    monkeypatch.setattr(secrets, "token_hex", lambda _: actual_token)
    secret_key = "testsecret"
    app = app_fn({"SECRET_KEY": secret_key})

    with app.app_context():
        encoded_token = generate_csrf_token()

    serializer = URLSafeTimedSerializer(secret_key, salt=CSRF_TOKEN_NAME)
    decoded_token = serializer.loads(encoded_token, max_age=CSRF_TOKEN_MAX_AGE)
    assert decoded_token == actual_token


def test_set_csrf_token(app):
    with app.test_request_context("/"):
        token = set_csrf_token()
        assert isinstance(token, str)
        assert CSRF_TOKEN_NAME in session
        assert CSRF_TOKEN_NAME in g


def test_unset_csrf_token(app):
    with app.test_request_context("/"):
        session[CSRF_TOKEN_NAME] = "test"
        setattr(g, CSRF_TOKEN_NAME, "test")
        unset_csrf_token()
        assert CSRF_TOKEN_NAME not in session
        assert CSRF_TOKEN_NAME not in g


def test_reset_csrf_token(app):
    with app.test_request_context("/"):
        before_token = "before"
        session[CSRF_TOKEN_NAME] = before_token
        setattr(g, CSRF_TOKEN_NAME, before_token)
        after_token = reset_csrf_token()
        assert isinstance(after_token, str)
        assert session[CSRF_TOKEN_NAME] != before_token
        assert g.get(CSRF_TOKEN_NAME) != before_token


def test_is_invalid_origin(app_fn):
    valid_origin = "http://example.com:80"
    invalid_origin = "http://evil.xyz:666"
    path = "/test/path"

    app = app_fn({"CSRF_TARGET_ORIGIN": valid_origin})
    with app.test_request_context(headers={"Origin": valid_origin}):
        assert not is_invalid_origin()

    app = app_fn({"CSRF_TARGET_ORIGIN": valid_origin})
    with app.test_request_context(headers={"Origin": invalid_origin}):
        assert is_invalid_origin()

    app = app_fn({"CSRF_TARGET_ORIGIN": valid_origin})
    with app.test_request_context(headers={"Referer": f"{valid_origin}{path}"}):
        assert not is_invalid_origin()

    app = app_fn({"CSRF_TARGET_ORIGIN": valid_origin})
    with app.test_request_context(headers={"Referer": f"{invalid_origin}{path}"}):
        assert is_invalid_origin()

    app = app_fn({"CSRF_TARGET_ORIGIN": valid_origin})
    with app.test_request_context():
        assert is_invalid_origin()


def test_is_invalid_csrf_token(app_fn):
    secret_key = "testsecret"
    app = app_fn({"SECRET_KEY": secret_key})

    with app.test_request_context():
        valid_csrf_token = generate_csrf_token()

    with app.test_request_context():
        assert is_invalid_csrf_token()

    with app.test_request_context():
        session[CSRF_TOKEN_NAME] = valid_csrf_token
        assert is_invalid_csrf_token()

    with app.test_request_context(headers={CSRF_TOKEN_NAME: valid_csrf_token}):
        assert is_invalid_csrf_token()

    with app.test_request_context(headers={CSRF_TOKEN_NAME: valid_csrf_token}):
        session[CSRF_TOKEN_NAME] = valid_csrf_token
        assert not is_invalid_csrf_token()

    with app.test_request_context():
        invalid_csrf_token = "invalid"

    with app.test_request_context(headers={CSRF_TOKEN_NAME: invalid_csrf_token}):
        session[CSRF_TOKEN_NAME] = valid_csrf_token
        assert is_invalid_csrf_token()

    with app.test_request_context(headers={CSRF_TOKEN_NAME: valid_csrf_token}):
        session[CSRF_TOKEN_NAME] = invalid_csrf_token
        assert is_invalid_csrf_token()

    with app.test_request_context():
        valid_csrf_token2 = generate_csrf_token()

    with app.test_request_context(headers={CSRF_TOKEN_NAME: valid_csrf_token2}):
        session[CSRF_TOKEN_NAME] = valid_csrf_token
        assert is_invalid_csrf_token()

    with app.test_request_context(headers={CSRF_TOKEN_NAME: valid_csrf_token}):
        session[CSRF_TOKEN_NAME] = valid_csrf_token2
        assert is_invalid_csrf_token()


def test_protect_request_from_csrf(app_fn):
    valid_origin = "http://example.com:80"
    invalid_origin = "http://evil.xyz:666"
    unsafe_method = "POST"
    path = "/"
    app = app_fn({"CSRF_TARGET_ORIGIN": valid_origin})

    for method in CSRF_SAFE_HTTP_METHODS:
        with app.test_request_context(method=method):
            assert protect_request_from_csrf() is None

    with app.test_request_context(
        headers={"Accept": "text/html", "Origin": invalid_origin},
        method=unsafe_method,
        path=path,
    ):
        response = protect_request_from_csrf()
        html = response[0]
        code = response[1]
        assert isinstance(html, str)
        assert code == HTTPStatus.FORBIDDEN.value

    with app.test_request_context(
        headers={"Accept": "application/json", "Origin": invalid_origin},
        method=unsafe_method,
        path=path,
    ):
        response = protect_request_from_csrf()
        json = response[0]
        code = response[1]
        assert isinstance(json["msg"], str)
        assert json["error_info"] == "INVALID_CSRF_TOKEN"
        assert code == HTTPStatus.FORBIDDEN.value
