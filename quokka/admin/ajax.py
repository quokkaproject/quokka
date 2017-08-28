# coding: utf-8
# TODO: adapt to tinymongo

# from flask_admin.contrib.mongoengine.ajax import QueryAjaxModelLoader
# from flask_admin.model.ajax import DEFAULT_PAGE_SIZE


# class AjaxModelLoader(object):  # QueryAjaxModelLoader):
#     """
#     """
#     def __init__(self, name, model, **options):
#         self.filters = options.pop('filters', None)
#         super(AjaxModelLoader, self).__init__(name, model, **options)

#     def get_list(self, term, offset=0, limit=DEFAULT_PAGE_SIZE):
#         query = self.model.objects

#         criteria = None

#         for field in self._cached_fields:
#             flt = {u'%s__icontains' % field.name: term}

#             if not criteria:
#                 criteria = mongoengine.Q(**flt)
#             else:
#                 criteria |= mongoengine.Q(**flt)

#         query = query.filter(criteria)

#         if self.filters:
#             query = query.filter(**self.filters)

#         if offset:
#             query = query.skip(offset)

#         return query.limit(limit).all()
