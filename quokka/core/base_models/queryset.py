
from mongoengine.queryset import QuerySet


class ExtendedQuerySet(QuerySet):

    def get_or_create(self, write_options=None, auto_save=True,
                      *q_objs, **query):
        """Retrieve unique object or create, if it doesn't exist. Returns a
        tuple of ``(object, created)``, where ``object`` is the retrieved or
        created object and ``created`` is a boolean specifying whether a new
        object was created. Raises
        :class:`~mongoengine.queryset.MultipleObjectsReturned` or
        `DocumentName.MultipleObjectsReturned` if multiple results are found.
        A new document will be created if the document doesn't exists; a
        dictionary of default values for the new document may be provided as a
        keyword argument called :attr:`defaults`.
        .. note:: This requires two separate operations and therefore a
            race condition exists.  Because there are no transactions in
            mongoDB other approaches should be investigated, to ensure you
            don't accidently duplicate data when using this method.  This is
            now scheduled to be removed before 1.0
        :param write_options: optional extra keyword arguments used if we
            have to create a new document.
            Passes any write_options onto :meth:`~mongoengine.Document.save`
        :param auto_save: if the object is to be saved automatically if
            not found.

        add to your documents:
        meta = {'queryset_class': ExtendedQuerySet}
        """
        defaults = query.get('defaults', {})
        if 'defaults' in query:
            del query['defaults']

        try:
            doc = self.get(*q_objs, **query)
            return doc, False
        except self._document.DoesNotExist:
            query.update(defaults)
            doc = self._document(**query)

            if auto_save:
                doc.save(write_options=write_options)
            return doc, True
