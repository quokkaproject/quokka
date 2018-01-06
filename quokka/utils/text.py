from slugify.main import Slugify

slugify = Slugify()
slugify.to_lower = True
slugify_category = Slugify()
slugify_category.to_lower = True
slugify_category.safe_chars = '/'


def abbreviate(name, pretty=False):
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
