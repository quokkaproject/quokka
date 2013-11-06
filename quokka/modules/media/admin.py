# coding : utf -8

from flask import url_for
from flask.ext.admin import form
from jinja2 import Markup

from quokka import admin
from quokka.core.admin import _, _l
from quokka.core.admin.models import ModelAdmin
from quokka.core.admin.fields import ImageUploadField
from quokka.utils.upload import dated_path, lazy_media_path
from .models import Image, File, Video, Audio, MediaGallery


class MediaAdmin(ModelAdmin):
    roles_accepted = ('admin', 'editor')
    column_list = ('title', 'path', 'published')
    form_columns = ['title', 'slug', 'path', 'channel', 'summary', 'published']

    form_overrides = {
        'path': form.FileUploadField
    }


class FileAdmin(MediaAdmin):
    form_args = {
        'path': {
            'label': 'File',
            'base_path': lazy_media_path(),
            'namegen': dated_path,
            'permission': 0o777
        }
    }


class VideoAdmin(FileAdmin):
    form_columns = ['title', 'slug', 'path', 'embed',
                    'channel', 'summary', 'published']


class AudioAdmin(FileAdmin):
    form_columns = ['title', 'slug', 'path', 'embed',
                    'channel', 'summary', 'published']


class ImageAdmin(MediaAdmin):
    roles_accepted = ('admin', 'editor')
    column_list = ('title', 'path', 'thumb', 'published')
    form_columns = ['title', 'slug', 'path', 'channel', 'summary', 'published']

    def _list_thumbnail(view, context, model, name):
        if not model.path:
            return ''

        return Markup(
            '<img src="%s">' % url_for(
                'media',
                filename=form.thumbgen_filename(model.path)
            )
        )

    column_formatters = {
        'thumb': _list_thumbnail
    }

    form_extra_fields = {
        'path': ImageUploadField(
            'Image',
            base_path=lazy_media_path(),
            thumbnail_size=(100, 100, True),
            endpoint="media",
            namegen=dated_path,
            permission=0o777,
            allowed_extensions="MEDIA_IMAGE_ALLOWED_EXTENSIONS",
        )
    }


class MediaGalleryAdmin(ModelAdmin):
    roles_accepted = ('admin', 'editor')


admin.register(File, FileAdmin, category=_('Media'), name=_l("File"))
admin.register(Video, VideoAdmin, category=_('Media'), name=_l("Video"))
admin.register(Audio, AudioAdmin, category=_('Media'), name=_l("Audio"))
admin.register(Image, ImageAdmin, category=_('Media'), name=_l("Image"))
admin.register(MediaGallery, MediaGalleryAdmin,
               category=_('Content'), name=_l("Media Gallery"))
