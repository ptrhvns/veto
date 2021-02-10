from http import HTTPStatus

from flask import render_template, request


def internal_server_error(e):
    msg = "Your request caused an unexpected error."
    code = HTTPStatus.INTERNAL_SERVER_ERROR.value

    if request.accept_mimetypes.accept_html:
        return render_template(f"errors/{code}.jinja", msg=msg), code
    else:
        return {"msg": msg}, code
