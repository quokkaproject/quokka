# coding : utf -8

from flask import url_for
from flask.ext.admin import form
from jinja2 import Markup

from quokka import admin
from quokka.utils.settings import get_setting_value
from quokka.core.models import Channel
from quokka.core.admin.models import ModelAdmin
from quokka.core.admin.fields import ImageUploadField
from quokka.utils.upload import dated_path, lazy_media_path
from quokka.core.admin.models import BaseContentAdmin
from quokka.core.widgets import TextEditor, PrepopulatedText
from .models import Image, File, Video, Audio, MediaGallery
from quokka.core.admin.ajax import AjaxModelLoader
from quokka.utils.translation import _l


class MediaAdmin(ModelAdmin):
    roles_accepted = ('admin', 'editor', 'author')
    column_list = ('title', 'path', 'published')
    form_columns = ['title', 'slug', 'path', 'channel', 'content_format',
                    'summary', 'comments_enabled', 'published']

    form_overrides = {
        'path': form.FileUploadField
    }

    form_args = {
        'summary': {'widget': TextEditor()},
        'slug': {'widget': PrepopulatedText(master='title')},
    }

    form_widget_args = {
        'channel': {'data-placeholder': _l('media/')}
    }


class FileAdmin(MediaAdmin):
    form_args = {
        'path': {
            'label': 'File',
            'base_path': lazy_media_path(),
            'namegen': dated_path,
            'permission': 0o777
        },
        'summary': {'widget': TextEditor()},
        'slug': {'widget': PrepopulatedText(master='title')},
    }

    form_ajax_refs = {
        'channel': AjaxModelLoader(
            'channel',
            Channel,
            fields=['title', 'slug', 'long_slug'],
            filters={"long_slug__startswith": "media/files"}
        )
    }


class VideoAdmin(FileAdmin):
    form_columns = ['title', 'slug', 'path', 'embed',
                    'channel', 'content_format',
                    'comments_enabled', 'summary', 'published']

    form_ajax_refs = {
        'channel': AjaxModelLoader(
            'channel',
            Channel,
            fields=['title', 'slug', 'long_slug'],
            filters={"long_slug__startswith": "media/video"}
        )
    }


class AudioAdmin(FileAdmin):
    form_columns = ['title', 'slug', 'path', 'embed',
                    'channel', 'content_format',
                    'comments_enabled', 'summary', 'published']

    form_ajax_refs = {
        'channel': AjaxModelLoader(
            'channel',
            Channel,
            fields=['title', 'slug', 'long_slug'],
            filters={"long_slug__startswith": "media/audio"}
        )
    }


class ImageAdmin(MediaAdmin):
    roles_accepted = ('admin', 'editor', 'author')
    column_list = ('title', 'path', 'thumb', 'published')
    form_columns = ['title', 'slug', 'path', 'channel', 'content_format',
                    'comments_enabled', 'summary', 'published']

    def _list_thumbnail(self, context, model, name):
        if not model.path:
            return ''

        return Markup(
            '<img src="%s" width="100">' % url_for(
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
            thumbnail_size=get_setting_value('MEDIA_IMAGE_THUMB_SIZE',
                                             default=(200, 200, True)),
            endpoint="media",
            namegen=dated_path,
            permission=0o777,
            allowed_extensions="MEDIA_IMAGE_ALLOWED_EXTENSIONS",
        )
    }

    form_ajax_refs = {
        'channel': AjaxModelLoader(
            'channel',
            Channel,
            fields=['title', 'slug', 'long_slug'],
            filters={"long_slug__startswith": "media/image"}
        )
    }


class MediaGalleryAdmin(BaseContentAdmin):
    roles_accepted = ('admin', 'editor', 'author')
    column_searchable_list = ('title', 'body', 'summary')

    form_columns = ['title', 'slug', 'channel', 'related_channels', 'summary',
                    'content_format', 'body',
                    'comments_enabled', 'published', 'add_image', 'contents',
                    'show_on_channel', 'available_at', 'available_until',
                    'tags', 'values', 'template_type']

    form_args = {
        'body': {'widget': TextEditor()},
        'slug': {'widget': PrepopulatedText(master='title')}
    }


admin.register(File, FileAdmin, category=_l('Media'), name=_l("File"))
admin.register(Video, VideoAdmin, category=_l('Media'), name=_l("Video"))
admin.register(Audio, AudioAdmin, category=_l('Media'), name=_l("Audio"))
admin.register(Image, ImageAdmin, category=_l('Media'), name=_l("Image"))
admin.register(MediaGallery, MediaGalleryAdmin,
               category=_l('Content'), name=_l("Media Gallery"))
