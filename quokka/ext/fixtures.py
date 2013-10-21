# coding: utf-8

from quokka.utils.populate import Populate
from quokka.core.models import Channel, Config, CustomValue, \
    SubContentPurpose, ChannelType


def configure(app, db):
    print("Loading fixtures")

    populate = Populate(db)

    if not SubContentPurpose.objects.count():
        populate.create_purposes()

    if not ChannelType.objects.count():
        populate.create_channel_types()

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
                CustomValue(name="site_name", rawvalue="A Quokka website",
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
