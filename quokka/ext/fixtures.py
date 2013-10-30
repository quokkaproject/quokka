# coding: utf-8

from quokka.utils.populate import Populate
from quokka.core.models import Quokka


def configure(app, db):

    try:
        is_installed = Quokka.objects.get(slug="is_installed")
    except:
        is_installed = False

    if not is_installed:
        print("Loading fixtures")
        populate = Populate(db)
        populate.create_configs()
        populate.create_purposes()
        populate.create_channel_types()
        populate.create_base_channels()
        Quokka.objects.create(slug="is_installed")
