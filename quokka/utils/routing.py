from flask import current_app
from .text import slugify


def expose(url='/', methods=('GET',)):
    """
        Use this decorator to expose views in your view classes.

        `url`
            Relative URL for the view
        `methods`
            Allowed HTTP methods. By default only GET is allowed.
    """
    def wrap(f):
        if not hasattr(f, '_urls'):
            f._urls = []
        f._urls.append((url, methods))
        return f

    return wrap


def get_content_url(content):
    category = content.get('category')
    title = content.get('title')
    slug = content.get('slug')
    ext = current_app.config.get('CONTENT_EXTENSION', 'html')
    if category:
        url = f'/{slugify(category)}/{slug or slugify(title)}.{ext}'
    else:
        url = f'/{slug or slugify(title)}.{ext}'
    return url
