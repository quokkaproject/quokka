from flask import request
from urllib.parse import urljoin
from slugify.main import Slugify

# slufigy for all strings
slugify = Slugify()
slugify.to_lower = True

# slugify isntance that keeps the `/`
slugify_category = Slugify()
slugify_category.to_lower = True
slugify_category.safe_chars = '/'


def abbreviate(name, pretty=False):
    """Abbreviate a name like Mickael Jonh Scott turns to Mickael J Scott"""
    names = name.split()
    if len(names) == 1:
        return name
    if len(names) == 2:
        return name
    result = [names[0]]
    tiny_name = False
    for surname in names[1:-1]:
        if len(surname) <= 3:
            result.append(surname)
            tiny_name = True
        else:
            if pretty and tiny_name:
                result.append(surname)
            else:
                result.append(surname[0] + '.')
            tiny_name = False
    result.append(names[-1])
    return ' '.join(result)


def normalize_var(text, s='_'):
    """replaces special chars from string value"""
    return text.replace(
        '/', s
    ).replace(
        '-', s
    ).replace(
        ' ', s
    ).replace(
        '@', s
    )


def make_social_link(network, txt):
    """from a name like `username` return http://social.com/username"""
    if txt.startswith(('http://', 'https://', 'www.')):
        return txt
    if '/' in txt:
        return f'http://{txt}'
    return f'{network}/{txt}'


def make_social_name(txt):
    """from a link like http://foo.com/username returns username"""
    return txt.split('/')[-1]


def cdata(data):
    """Wraps items in CDATA tag"""
    if not data:
        return ""
    return f"<![CDATA[\n{data}\n]]>"


def make_external_url(url):
    """Joins item URL with external URL"""
    return urljoin(request.url_root, url)


def split_all_category_roots(cat):
    """Takes category like `foo/bar/baz` and returns its roots
    ex: ['foo/bar/baz', 'foo/bar', 'foo']
    """
    if cat and '/' in cat:
        cats = [cat]
        is_root = False
        raw = cat
        while not is_root:
            item = [part for part in raw.rpartition('/') if part]
            raw = item[0]
            cats.append(raw)
            if len(item) == 1:
                is_root = True
        return cats
    else:
        return [cat]
