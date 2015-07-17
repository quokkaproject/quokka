# coding: utf-8
import logging
from quokka.utils.populate import Populate
from quokka.core.models import Quokka


logger = logging.getLogger()


def configure(app, db):

    try:
        is_installed = Quokka.objects.get(slug="is_installed")
    except:
        is_installed = False

    if not is_installed:
        print("Loading fixtures")
        populate = Populate(db, filepath=app.config.get('POPULATE_FILEPATH'))
        populate.create_configs()
        populate.create_purposes()
        populate.create_channel_types()
        populate.create_base_channels()
        try:
            with app.test_request_context():
                user_data, user_obj = populate.create_initial_superuser()
                populate.create_initial_post(user_data, user_obj)
        except:
            logger.warning("Could not create initial user and post")
        Quokka.objects.create(slug="is_installed")
