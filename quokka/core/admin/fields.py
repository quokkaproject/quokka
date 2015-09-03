# coding: utf-8
import random
import sys

from werkzeug.datastructures import FileStorage
from flask import current_app
from flask.ext.admin import form
from flask.ext.admin.form.upload import ImageUploadInput
from flask.ext.admin._compat import urljoin

from quokka.core.models import SubContent, SubContentPurpose
from quokka.modules.media.models import Image

if sys.version_info.major == 3:
    unicode = lambda x: u'{}'.format(x)  # noqa  # flake8: noqa


class ThumbWidget(ImageUploadInput):
    empty_template = ""
    data_template = ('<div class="image-thumbnail">'
                     ' <img %(image)s>'
                     '</div>')

    def get_url(self, field):
        if field.thumbnail_size:
            filename = field.thumbnail_fn(field.data)
        else:
            filename = field.data

        if field.url_relative_path:
            filename = urljoin(field.url_relative_path, filename)

        return field.data


class ThumbField(form.ImageUploadField):
    widget = ThumbWidget()


class ImageUploadField(form.ImageUploadField):
    def is_file_allowed(self, filename):
        extensions = self.allowed_extensions  # noqa
        if isinstance(extensions, (str, unicode)) and extensions.isupper():
            items = current_app.config.get(extensions, extensions)
            merged_items = [
                item.lower() for item in items
            ] + [item.upper() for item in items]
            self.allowed_extensions = merged_items
        return super(ImageUploadField, self).is_file_allowed(filename)


class ContentImageField(ImageUploadField):
    def populate_obj(self, obj, name):
        pass

    def save_contents(self, obj):
        # field = getattr(obj, name, None)
        # if field:
        #     # If field should be deleted, clean it up
        #     if self._should_delete:
        #         self._delete_file(field)
        #         setattr(obj, name, None)
        #         return

        new_image = Image(
            title=u"Image: {0}".format(obj.title),
            slug=u"{0}-{1}".format(obj.slug, random.getrandbits(8)),
            channel=Image.get_default_channel(),
            published=True
        )
        if self.data and isinstance(self.data, FileStorage):
            # if field:
            #     self._delete_file(field)

            filename = self.generate_name(new_image, self.data)
            filename = self._save_file(self.data, filename)

            setattr(new_image, 'path', filename)

            new_image.save()

            if obj.contents.filter(identifier='mainimage'):
                purpose = SubContentPurpose.objects.get(identifier='image')
            else:
                purpose = SubContentPurpose.objects.get(
                    identifier='mainimage'
                )

            subcontent = SubContent(
                content=new_image,
                purpose=purpose,
            )

            obj.contents.append(subcontent)
            obj.save()
