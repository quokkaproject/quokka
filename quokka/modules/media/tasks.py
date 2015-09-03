# coding: utf-8

from __future__ import print_function
from quokka import create_celery_app

celery = create_celery_app()


@celery.task
def media_task():
    print("Doing something async...")  # noqa
