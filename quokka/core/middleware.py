# -*- coding: utf-8 -*-

from werkzeug import url_decode


class HTTPMethodOverrideMiddleware(object):
    """The HTTPMethodOverrideMiddleware middleware implements the hidden HTTP
    method technique. Not all web browsers support every HTTP method, such as
    DELETE and PUT. This middleware class allows clients to provide a method
    override parameter via an HTTP header value or a querystring parameter.
    This middleware will look for the header paramter first followed by the
    querystring. The default HTTP header name is `X-HTTP-METHOD-OVERRIDE` and
    the default querystring parameter name is `__METHOD__`.
    These can be changed via the constructor parameters `header_name`
    and `querystring_param`respectively.
    Additionally, a list of allowed HTTP methods may be specified
    via the `allowed_methods` constructor parameter.
    The default allowed methods are GET, HEAD, POST, DELETE, PUT, PATCH,
    and OPTIONS.
    """

    bodyless_methods = frozenset(['GET', 'HEAD', 'OPTIONS', 'DELETE'])

    def __init__(self, app, header_name=None,
                 querystring_param=None, allowed_methods=None):
        header_name = header_name or 'X-HTTP-METHOD-OVERRIDE'

        self.app = app
        self.header_name = 'HTTP_' + header_name.replace('-', '_')
        self.querystring_param = querystring_param or '__METHOD__'
        self.allowed_methods = frozenset(
            allowed_methods or
            ['GET', 'HEAD', 'POST', 'DELETE', 'PUT', 'PATCH', 'OPTIONS']
        )

    def _get_from_querystring(self, environ):
        if self.querystring_param in environ.get('QUERY_STRING', ''):
            args = url_decode(environ['QUERY_STRING'])
            return args.get(self.querystring_param)
        return None

    def _get_method_override(self, environ):
        return environ.get(self.header_name, None) or \
            self._get_from_querystring(environ) or ''

    def __call__(self, environ, start_response):
        method = self._get_method_override(environ).upper()

        if method in self.allowed_methods:
            method = method.encode('ascii', 'replace')
            environ['REQUEST_METHOD'] = method

        if method in self.bodyless_methods:
            environ['CONTENT_LENGTH'] = '0'

        return self.app(environ, start_response)
