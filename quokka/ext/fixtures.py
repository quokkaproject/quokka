# coding: utf-8
from quokka.utils.populate import Populate
from quokka.core.models.config import Quokka


def configure(app, db):

    try:
        is_installed = Quokka.objects.get(slug="is_installed")
    except:
        is_installed = False

    if not is_installed:
        app.logger.info("Loading fixtures")
        populate = Populate(
            db,
            filepath=app.config.get('POPULATE_FILEPATH'),
            first_install=True
        )
        try:
            populate.create_configs()
            populate.create_purposes()
            populate.create_channel_types()
            populate.create_base_channels()
            populate.role("admin")
            populate.role("author")
            try:
                with app.app_context():
                    user_data, user_obj = populate.create_initial_superuser()
                    populate.create_initial_post(user_data, user_obj)
            except Exception as e:
                app.logger.warning("Cant create initial user and post: %s" % e)
        except Exception as e:
            app.logger.error("Error loading fixtures: %s" % e)
            populate.reset()
        else:
            Quokka.objects.create(slug="is_installed")
