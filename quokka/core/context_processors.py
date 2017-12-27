from .content.models import make_model, Category
from .content.utils import url_for_content


def configure(app):

    # add context processors
    @app.context_processor
    def app_theme_context():
        context = {**app.theme_context}
        if app.theme_context.get('DISPLAY_RECENT_POSTS_ON_SIDEBAR'):
            context['articles'] = [
                make_model(item)
                for item in app.db.article_set({'published': True})
            ]

        context['pages'] = [
            make_model(item) for item in app.db.page_set({'published': True})
        ]
        # app.theme_context['PAGES']
        # app.theme_context['tags']

        # TODO: Split categories by `/` to get roots
        context['categories'] = [
            (Category(cat), [])
            for cat in app.db.value_set(
                'index', 'category',
                filter={'published': True},
                sort=True
            )
        ]
        # context['tag_cloud']

        for menublock in app.theme_context.get('MENUBLOCKS'):
            menu = build_menu(app, menublock)
            if menu:
                context[menublock] = menu

        for textblock in app.theme_context.get('TEXTBLOCKS'):
            block = get_text_block(app, textblock)
            if block:
                context[textblock] = block

        return context


def build_menu(app, title='MENUITEMS'):
    menu = app.db.get(
        'index',
        {'content_type': 'block', 'title': title, 'published': True}
    )
    if menu and menu.get('block_items'):
        return [
            build_menu_item(app, item) for item in menu['block_items']
        ]


def build_menu_item(app, item):
    """Return a name for menu item based on its destination"""
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
                [build_menu_item(app, subitem)
                 for subitem in content['block_items']]
            )

        return (name or content['title'], url_for_content(content))

    for ref in ['author', 'category', 'tag']:
        data = item.get(f"{ref}_id")
        if not data:
            continue
        return (name or data, make_model(data, ref).url)

    return (name, item['item'])


def get_text_block(app, title):
    block = app.db.get(
        'index',
        {'content_type': 'block', 'title': title, 'published': True}
    )
    if block:
        return make_model(block).content
