# coding: utf-8
from flask import render_template


def configure(app):
    if app.config.get('DEBUG') is True:
        app.logger.debug('Skipping error handlers in Debug mode')
        return

    @app.errorhandler(403)
    def forbidden_page(*args, **kwargs):
        """
        The server understood the request, but is refusing to fulfill it.
        Authorization will not help and the request SHOULD NOT be repeated.
        If the request method was not HEAD and the server wishes to make public
        why the request has not been fulfilled, it SHOULD describe the
        reason for
        the refusal in the entity. If the server does not wish to make this
        information available to the client, the status code 404 (Not Found)
        can be used instead.
        """
        return render_template("errors/access_forbidden.html"), 403

    @app.errorhandler(404)
    def page_not_found(*args, **kwargs):
        """
        The server has not found anything matching the Request-URI.
        No indication
        is given of whether the condition is temporary or permanent.
        The 410 (Gone)
        status code SHOULD be used if the server knows, through some internally
        configurable mechanism, that an old resource is permanently unavailable
        and has no forwarding address. This status code is commonly used when
        the
        server does not wish to reveal exactly why the request has been
        refused,
        or when no other response is applicable.
        """
        return render_template("errors/page_not_found.html"), 404

    @app.errorhandler(405)
    def method_not_allowed_page(*args, **kwargs):
        """
        The method specified in the Request-Line is not allowed for the
        resource
        identified by the Request-URI. The response MUST include an
        Allow header
        containing a list of valid methods for the requested resource.
        """
        return render_template("errors/method_not_allowed.html"), 405

    @app.errorhandler(500)
    def server_error_page(*args, **kwargs):
        return render_template("errors/server_error.html"), 500

    # URLBUILD Error Handlers
    def admin_icons_error_handler(error, endpoint, *args, **kwargs):
        "when some of default dashboard button is deactivated, avoids error"
        if endpoint in [item[0] for item in app.config.get('ADMIN_ICONS', [])]:
            return '/admin'
        raise error

    app.url_build_error_handlers.append(admin_icons_error_handler)
