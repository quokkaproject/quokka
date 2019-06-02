from quokka.utils.text import slugify_category, slugify
from flask import current_app as app


def url_for_content(content, include_ext=True):
    """Return a relative URL for content dict or Content model
    """
    if not isinstance(content, dict):
        data = content.data
    else:
        data = content

    category_slug = (
        data.get('category_slug') or
        slugify_category(data.get('category') or '')
    )
    slug = data.get('slug') or slugify(data.get('title'))

    if category_slug:
        slug = f'{category_slug}/{slug}'

    content_type = data.get('content_type')
    if content_type not in (None, 'article', 'page'):
        slug = f'{content_type}/{slug}'

    if not include_ext:
        return slug

    ext = app.config.get("CONTENT_EXTENSION", "html")
    if data.get('published'):
        # return url_for('quokka.core.content.detail', slug=slug)
        return f'{slug}.{ext}'
    else:
        # return url_for('quokka.core.content.preview', slug=slug)
        return f'{slug}.preview'


# TODO: remove this and use model
def url_for_category(category):
    # TODO: handle extension for static site
    # ext = app.config.get("CONTENT_EXTENSION", "html")
    if isinstance(category, str):
        return slugify_category(category)
    return category.url


def strftime(value, dtformat):
    return value.strftime(dtformat)
