from .content.models import make_model, Category
from quokka.utils.blocks import build_menu, get_text_block, get_quokka_home


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

        context['categories'] = [
            (Category(cat), [])
            for cat in app.db.category_set(filter={'published': True})
        ]
        # context['tag_cloud']

        for menublock in app.theme_context.get('MENUBLOCKS'):
            menu = build_menu(menublock)
            if menu:
                context[menublock] = menu

        for textblock in app.theme_context.get('TEXTBLOCKS'):
            block = get_text_block(textblock)
            if block:
                context[textblock] = block

        quokka_home = get_quokka_home()
        if quokka_home:
            context[
                f"{app.theme_context['ACTIVE'].upper()}_HOME"
            ] = quokka_home
            context['QUOKKA_HOME'] = quokka_home

        return context
