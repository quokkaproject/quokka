# coding: utf -8

from flask.ext.admin.babel import gettext, ngettext, lazy_gettext


def _(*args, **kwargs):
    return gettext(*args, **kwargs)


def _l(*args, **kwargs):
    return lazy_gettext(*args, **kwargs)


def _s(*args, **kwargs):
    return ngettext(*args, **kwargs)
