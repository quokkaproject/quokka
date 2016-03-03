from flask import (
    redirect, url_for, request, current_app, render_template_string, abort
)
from flask.globals import _app_ctx_stack, _request_ctx_stack
from werkzeug.urls import url_parse
from quokka.core.templates import render_template


def dispatch_aliases():
    """
    When ALIASES_ENABLED == True

    This method handle 3 QuokkaCMS features:
    1. Fixed aliases
      Alias is defined in ALIASES_MAP setting as a dictionary
    2. Managed Redirects
      Alias defined in database
    3. Channel and Content aliases
      Alias defined in specific channel or content

    ALIASES_MAP
    keys are long_slug
        keys should always start with /
        & end with / or extension.
    {
        "/team/": {
            "alias_type": "endpoint|long_slug|url|string|template",
            "action": "redirect|render",
            "to": "authors|/articles/science.html|http://t.co|'<b>Hello</b>'",
            "published": True,
            "available_at": "",
            "available_until: "",
        }
    }

    - 'endpoint' and 'long_slug' by default are rendered
    - 'url' is always redirect
    - 'string' and 'template' are always rendered
    """

    app = current_app
    aliases_map = app.config.get('ALIASES_MAP')
    if aliases_map and request.path in aliases_map:
        alias = aliases_map[request.path]
        status = alias.get('status', 200)
        if alias['alias_type'] == 'endpoint':
            endpoint = alias['to']
            if alias.get('action') == 'redirect':
                return redirect(url_for(endpoint, **request.args))
            else:  # render
                return app.process_response(
                    app.make_response(
                        app.view_functions[endpoint]()
                    )
                )
        elif alias['alias_type'] == 'long_slug':
            long_slug = alias['to']
            if alias.get('action') == 'redirect':
                return redirect(long_slug)  # pass request.args ?
            else:  # render
                endpoint = route_from(long_slug)[0]
                return app.process_response(
                    app.make_response(
                        app.view_functions[endpoint]()
                    )
                )
        elif alias['alias_type'] == 'url':
            return redirect(alias['to'])
        elif alias['alias_type'] == 'string':
            return render_template_string(alias['to']), status
        elif alias['alias_type'] == 'template':
            return render_template(alias['to']), status


def route_from(url, method=None):
    appctx = _app_ctx_stack.top
    reqctx = _request_ctx_stack.top
    if appctx is None:
        raise RuntimeError('Attempted to match a URL without the '
                           'application context being pushed. This has to be '
                           'executed when application context is available.')

    if reqctx is not None:
        adapter = reqctx.url_adapter
    else:
        adapter = appctx.url_adapter
        if adapter is None:
            raise RuntimeError('Application was not able to create a URL '
                               'adapter for request independent URL matching. '
                               'You might be able to fix this by setting '
                               'the SERVER_NAME config variable.')
    parsed = url_parse(url)
    if parsed.netloc is not "" and parsed.netloc != adapter.server_name:
        abort(404)
    return adapter.match(parsed.path, method)
