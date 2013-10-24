# coding: utf-8
import random
import os.path as op
from werkzeug import secure_filename
from flask import current_app
from datetime import date
from speaklater import make_lazy_string


def dated_path(obj, file_data):
    try:
        prefix = getattr(obj, 'model_name')
    except:
        prefix = "undefined"

    parts = op.splitext(file_data.filename)
    rand = random.getrandbits(16)
    filename = u"{name}_{rand}{ext}".format(
        rand=rand, name=parts[0], ext=parts[1]
    )
    filename = secure_filename(filename)
    today = date.today()
    path = u"{prefix}/{t.year}/{t.month}/{filename}".format(
        prefix=prefix, t=today, filename=filename, r=random.getrandbits(32)
    )
    return path


def media_path(suffix=None):
    media_root = current_app.config.get('MEDIA_ROOT')
    if suffix:
        return op.join(media_root, suffix)
    return op.join(media_root)


def lazy_media_path(suffix=None):
    return make_lazy_string(lambda: media_path(suffix))
