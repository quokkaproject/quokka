#coding: utf-8
from flask import current_app
from flask.ext.admin import form


class ImageUploadField(form.ImageUploadField):
    def is_file_allowed(self, filename):
        extensions = self.allowed_extensions
        if isinstance(extensions, (str, unicode)) and extensions.isupper():
            items = current_app.config.get(extensions, extensions)
            self.allowed_extensions = items
        return super(ImageUploadField, self).is_file_allowed(filename)
