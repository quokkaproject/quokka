# coding: utf-8

from quokka.utils.populate import Populate
from quokka.core.models import Config, CustomValue


def configure(app, db):
    print("Loading fixtures")

    populate = Populate(db)
    populate.create_purposes()
    populate.create_channel_types()
    populate.create_base_channels()

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
