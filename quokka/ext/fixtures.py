# coding: utf-8

from quokka.utils.populate import Populate


def configure(app, db):
    print("Loading fixtures")

    populate = Populate(db)
    populate.create_configs()
    populate.create_purposes()
    populate.create_channel_types()
    populate.create_base_channels()
