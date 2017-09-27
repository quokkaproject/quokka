from quokka.utils.text import slugify_category
from flask import current_app as app


def url_for_content(content):
    """Return a relative URL for content dict or Content model
    """
    if not isinstance(content, dict):
        data = content.data
    else:
        data = content

    category_slug = data.get('category_slug')
    slug = data.get('slug')
    published = data.get('published')

    if category_slug:
        slug = f'{category_slug}/{slug}'

    ext = app.config.get("CONTENT_EXTENSION", "html")

    if published:
        # return url_for('quokka.core.content.detail', slug=slug)
        return f'{slug}.{ext}'
    else:
        # return url_for('quokka.core.content.preview', slug=slug)
        return f'{slug}.preview'


def url_for_category(category):
    # TODO: handle extension for static site
    # ext = app.config.get("CONTENT_EXTENSION", "html")
    if isinstance(category, str):
        return slugify_category(category)
    return category.url


def strftime(value, dtformat):
    return value.strftime(dtformat)
