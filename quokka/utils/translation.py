from flask import g
from babel.support import LazyProxy
from flask.ext.babelex import Domain

# from quokka.utils.translations import ugettext_lazy as _


def ugettext(s):
    # we assume a before_request function
    # assigns the correct user-specific
    # translations
    return g.translations.ugettext(s)

ugettext_lazy = LazyProxy(ugettext)

domain = Domain()
_l = domain.lazy_gettext
_ = domain.gettext
_n = domain.ngettext
