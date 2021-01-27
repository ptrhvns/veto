from flask import render_template, request


def internal_server_error(e):
    msg = "We couldn't fulfill your request due to an unexpected error."
    code = 500

    if request.accept_mimetypes.accept_html:
        return render_template("errors/500.jinja", msg=msg), code
    else:
        return {"msg": msg}, code
