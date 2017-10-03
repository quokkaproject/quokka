from .echo import green, lecho, red


def fetch_theme(theme, destiny):
    """TODO: implement this"""
    lecho('🎨  Warning', f'{theme} theme not installed', red)
    return
    if theme:
        lecho('🎨  Theme installed', theme, green)


def fetch_modules(modules, destiny):
    """TODO: implement this"""
    lecho('🚚  Warning', f'{modules} modules not installed', red)
    return
    if modules:
        lecho('🚚  Modules installed', modules, green)


def cookiecutter(*args, **kwargs):
    lecho('🔧  Warning:', 'Config file not written', red)
