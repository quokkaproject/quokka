from flask import g
from babel.support import LazyProxy
from flask.ext.babelex import gettext, lazy_gettext, ngettext

# from quokka.utils.translations import ugettext_lazy as _


def ugettext(s):
    # we assume a before_request function
    # assigns the correct user-specific
    # translations
    return g.translations.ugettext(s)

ugettext_lazy = LazyProxy(ugettext)

_ = gettext
_l = lazy_gettext
_n = ngettext
