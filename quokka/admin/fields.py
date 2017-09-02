# coding: utf-8
# import random
# import sys

# from flask import current_app
from flask_admin import form
from flask_admin.form.upload import ImageUploadInput

# from werkzeug.datastructures import FileStorage


class SmartSelect2Field(form.Select2Field):

    def iter_choices(self):
        """
        We should update how choices are iter to make sure that value from
        internal list or tuple should be selected.
        """
        if self.allow_blank:
            yield (u'__None', self.blank_text, self.data is None)

        for value, label in self.concrete_choices:
            yield (value, label, self.coerce(value) == self.data)

        # for value, label in self.concrete_choices:
        #     yield (value, label, (self.coerce, self.data))

    @property
    def concrete_choices(self):
        if callable(self.choices):
            return self.choices()
        return self.choices

    @property
    def choice_values(self):
        return [value for value, label in self.concrete_choices]

    def pre_validate(self, form):
        if self.allow_blank and self.data is None:
            return

        values = self.choice_values
        if (self.data is None and u'' in values) or self.data in values:
            return True

        super(SmartSelect2Field, self).pre_validate(form)


class ThumbWidget(ImageUploadInput):
    empty_template = ""
    data_template = ('<div class="image-thumbnail">'
                     ' <img %(image)s>'
                     '</div>')


class ThumbField(form.ImageUploadField):
    widget = ThumbWidget()


# class ImageUploadField(form.ImageUploadField):
#     def is_file_allowed(self, filename):
#         extensions = self.allowed_extensions  # noqa
#         if isinstance(extensions, (str, unicode)) and extensions.isupper():
#             items = current_app.config.get(extensions, extensions)
#             merged_items = [
#                 item.lower() for item in items
#             ] + [item.upper() for item in items]
#             self.allowed_extensions = merged_items
#         return super(ImageUploadField, self).is_file_allowed(filename)


class ContentImageField(form.ImageUploadField):

    def populate_obj(self, obj, name):
        pass

    # def save_contents(self, obj):
    #     # field = getattr(obj, name, None)
    #     # if field:
    #     #     # If field should be deleted, clean it up
    #     #     if self._should_delete:
    #     #         self._delete_file(field)
    #     #         setattr(obj, name, None)
    #     #         return

    #     new_image = Image(
    #         title=u"Image: {0}".format(obj.title),
    #         slug=u"{0}-{1}".format(obj.slug, random.getrandbits(8)),
    #         channel=Image.get_default_channel(),
    #         published=True
    #     )
    #     if self.data and isinstance(self.data, FileStorage):
    #         # if field:
    #         #     self._delete_file(field)

    #         filename = self.generate_name(new_image, self.data)
    #         filename = self._save_file(self.data, filename)

    #         setattr(new_image, 'path', filename)

    #         new_image.save()

    #         if obj.contents.filter(identifier='mainimage'):
    #             purpose = SubContentPurpose.objects.get(identifier='image')
    #         else:
    #             purpose = SubContentPurpose.objects.get(
    #                 identifier='mainimage'
    #             )

    #         subcontent = SubContent(
    #             content=new_image,
    #             purpose=purpose,
    #         )

    #         obj.contents.append(subcontent)
    #         obj.save()
