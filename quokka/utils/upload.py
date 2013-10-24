# coding: utf-8
import random
import os.path as op
from werkzeug import secure_filename
from flask import current_app
from datetime import date
from .text import LazyString


def dated_path(obj, file_data):
    try:
        prefix = getattr(obj, 'model_name')
    except:
        prefix = ""

    parts = op.splitext(file_data.filename)
    rand = random.getrandbits(16)
    filename = u"{prefix}_{rand}_{name}{ext}".format(
        prefix=prefix, rand=rand, name=parts[0], ext=parts[1]
    )
    filename = secure_filename(filename)
    today = date.today()
    path = u"{t.year}/{t.month}/{filename}".format(
        t=today, filename=filename, r=random.getrandbits(32)
    )
    return path


def media_path(suffix=None):
    return op.join(current_app.config.get('MEDIA_ROOT'), suffix)


def lazy_media_path(suffix=None):
    return LazyString(lambda: media_path(suffix))
