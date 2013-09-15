# coding: utf-8

from quokka.core.models import Channel, Config, CustomValue


def configure(app):
    print("Loading fixtures")
    if not Channel.objects.count():
        # Create homepage if it does not exists
        Channel.objects.create(
            title="home",
            slug="home",
            description="App homepage",
            is_homepage=True,
            include_in_rss=True,
            indexable=True,
            show_in_menu=True,
            canonical_url="/",
            order=0,
            published=True,
        )

    if not Config.objects.count():
        Config.objects.create(
            group="global",
            description="Global preferences for the website",
            values=[
                CustomValue(name="example", rawvalue="example_value",
                            format="text")
            ]
        )
        Config.objects.create(
            group="settings",
            description="This values overrides app settings (CAUTION!!!)",
            values=[
                CustomValue(name="DEFAULT_THEME", rawvalue="default",
                            format="text")
            ]
        )
