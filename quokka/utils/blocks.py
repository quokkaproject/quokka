from flask import current_app
from quokka.core.content.utils import url_for_content
from quokka.core.content.models import make_model


def get_block(title, app=None):
    app = app or current_app
    return app.db.get(
        'index',
        {'content_type': 'block', 'title': title, 'published': True}
    )


def get_blocks(app=None, *args, **kwargs):
    app = app or current_app
    return app.db.block_set(*args, **kwargs)


def build_menu(title='MENUITEMS', app=None):
    app = app or current_app
    menu = app.db.get(
        'index',
        {'content_type': 'block', 'title': title, 'published': True}
    )
    if menu and menu.get('block_items'):
        return [
            build_menu_item(item) for item in menu['block_items']
        ]


def build_menu_item(item, app=None):
    """Return a name for menu item based on its destination"""
    app = app or current_app
    dropdown_enabled = app.theme_context.get('MENU_DROPDOWN_ENABLED', False)
    name = item.get('name')

    if item.get('index_id'):
        content = app.db.get('index', {'_id': item['index_id']})

        if (
            dropdown_enabled and
            item.get('item_type') == 'dropdown' and
            content['content_type'] == 'block'
        ):
            return (
                name or content['title'],
                [build_menu_item(subitem)
                 for subitem in content['block_items']]
            )

        return (name or content['title'], url_for_content(content))

    for ref in ['author', 'category', 'tag']:
        data = item.get(f"{ref}_id")
        if not data:
            continue
        return (name or data, make_model(data, ref).url)

    return (name, item['item'])


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
        {'title': item['name']}
        for item in quokka_home.get('block_items', [])
    ]
