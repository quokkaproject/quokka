# coding: utf-8
from quokka.utils.blocks import get_block, get_blocks, get_block_by_id


def is_list(obj):
    return isinstance(obj, (list, tuple))


def configure(app):
    """Configure Jinja filters and globals"""
    # app.jinja_env.filters['isinstance'] = is_instance
    app.add_template_global(is_list)
    app.add_template_global(get_block)
    app.add_template_global(get_block_by_id)
    app.add_template_global(get_blocks)
