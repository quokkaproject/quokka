import logging


def configure(app):
    if app.config.get("LOGGER_ENABLED"):
        logging.basicConfig(
            level=getattr(logging, app.config.get("LOGGER_LEVEL", "DEBUG")),
            format=app.config.get(
                "LOGGER_FORMAT",
                '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'),
            datefmt=app.config.get("LOGGER_DATE_FORMAT", '%d.%m %H:%M:%S')
        )
