# -*- coding: utf-8 -*-


from __future__ import print_function
from quokka import create_celery_app

celery = create_celery_app()


@celery.task
def send_manager_added_email(*recipients):
    print('sending manager added email...')  # noqa


@celery.task
def send_manager_removed_email(*recipients):
    print('sending manager removed email...')  # noqa
