from flask import current_app
from quokka.core.content.models import make_model


def get_block(title, app=None):
    app = app or current_app
    block = app.db.get(
        'index',
        {'content_type': 'block', 'title': title, 'published': True}
    )
    if block:
        return make_model(block)


def get_block_by_id(_id, app=None):
    app = app or current_app
    block = app.db.get(
        'index',
        {'content_type': 'block', '_id': _id, 'published': True}
    )
    if block:
        return make_model(block)


def get_blocks(app=None, *args, **kwargs):
    app = app or current_app
    blocks = app.db.block_set(*args, **kwargs)
    if blocks:
        return [make_model(block) for block in blocks]


def build_menu(title='MENUITEMS', app=None):
    app = app or current_app
    menu = get_block(title, app)
    if menu and menu.block_items:
        ret = [
            build_menu_item(block_item) for block_item in menu.block_items
        ]
        return ret


def build_menu_item(block_item, app=None):
    """Return a name for menu item based on its destination"""
    app = app or current_app
    dropdown_enabled = app.theme_context.get('MENU_DROPDOWN_ENABLED', False)
    if dropdown_enabled and block_item.is_block and block_item.is_dropdown:
        return (
            block_item.name,
            [build_menu_item(subitem)
             for subitem in block_item.item.block_items]
        )
    return (block_item.name, block_item.url)


def get_text_block(title, app=None):
    app = app or current_app
    block = app.db.get(
        'index',
        {'content_type': 'block', 'title': title, 'published': True}
    )
    if block:
        return make_model(block).content


def get_quokka_home(app=None):
    app = app or current_app
    quokka_home = get_block('QUOKKA_HOME')
    if not quokka_home:
        return
    return [
        {
            'title': block_item.name,
            'text': block_item.item.content,
            'items': [
                {
                    'title': subitem.name,
                    'action': [
                        subitem.get('action_text', 'read more'), subitem.url
                    ],
                    **subitem.metadata
                }
                for subitem in block_item.item.block_items
            ],
            **block_item.metadata

        }
        for block_item in quokka_home.block_items
    ]
