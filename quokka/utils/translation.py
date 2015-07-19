from flask import g
from babel.support import LazyProxy

# from quokka.utils.translations import ugettext_lazy as _


def ugettext(s):
    # we assume a before_request function
    # assigns the correct user-specific
    # translations
    return g.translations.ugettext(s)

ugettext_lazy = LazyProxy(ugettext)
