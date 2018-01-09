# -*- coding: utf-8 -*-
"""
# ext_list = '|'.join(app.config.get(
#     "CONTENT_EXTENSION_LIST", ['html', 'htm', 'rss', 'atom']))
# ext = f'<regex("(?!.*[.])((?:{ext_list})).*$"):ext>'
# ext = f'<regex("(?!.*[.])((?:html|rss|atom)).*$"):ext>'

@app.route('/foo/bar/<regex("regexhere"):name>/baz/<int:number>)
"""

from werkzeug.routing import BaseConverter


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


class Regex(object):
    """ Enables Flask Regex Routes """

    def __init__(self, app=None):
        self.app = app

        if self.app:
            self.init_app(self.app)

    def init_app(self, app):
        """ Configures the Regex Converter """

        app.url_map.converters['regex'] = RegexConverter
