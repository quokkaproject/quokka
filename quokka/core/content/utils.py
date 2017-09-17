
def url_for_content(content):
    """Return a relative URL for content dict or Content model
    """
    if not isinstance(content, dict):
        data = content.data
    else:
        data = content

    category = data.get('category')
    slug = data.get('slug')
    published = data.get('published')

    if category:
        slug = f'{category}/{slug}'

    if published:
        # return url_for('quokka.core.content.detail', slug=slug)
        return f'{slug}.html'
    else:
        # return url_for('quokka.core.content.preview', slug=slug)
        return f'{slug}.preview'


def url_for_category(category):
    # TODO: dyamize this
    return f'{category}/'


def strftime(value, dtformat):
    return value.strftime(dtformat)
