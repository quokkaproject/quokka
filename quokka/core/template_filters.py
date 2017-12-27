# coding: utf-8


def is_list(obj):
    return isinstance(obj, (list, tuple))


def configure(app):
    """Configure Jinja filters and globals"""
    # app.jinja_env.filters['isinstance'] = is_instance
    app.add_template_global(is_list)
