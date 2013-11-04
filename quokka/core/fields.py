# coding: utf-8

from mongoengine import fields
from mongoengine.base.datastructures import BaseList


class MultipleObjectsReturned(Exception):
    pass


def match_all(i, kwargs):
    return all([getattr(i, k) == v for k, v in kwargs.items()])


def getinstance(_instance):
    return _instance.__class__.objects.get(pk=_instance.pk)


def only_matches(obj, kwargs, silent=True):
    if not kwargs and silent:
        return obj
    return filter(lambda i: match_all(i, kwargs), obj)


def _exclude(self):
    def inner(*args, **kwargs):
        _values = only_matches(self, kwargs, silent=False)
        values = [item for item in self if item not in _values]
        return FilteredList(values, getinstance(self._instance), self._name)
    return inner


def _filter(self):
    def inner(*args, **kwargs):
        values = only_matches(self, kwargs)
        return FilteredList(values, getinstance(self._instance), self._name)
    return inner


def _get(self):
    def inner(*args, **kwargs):
        values = only_matches(self, kwargs)
        if len(values) > 1:
            raise MultipleObjectsReturned("More than one object returned")
        return values and values[0]
    return inner


def _delete(self):
    def inner(*args, **kwargs):
        values = only_matches(self, kwargs)
        for item in values:
            self.remove(item)
        self._instance.save()
        self._instance.reload()
        if len(values) > 1:
            return FilteredList(values,
                                getinstance(self._instance),
                                self._name)
        else:
            return values and values[0]
    return inner


def _create(self):
    def inner(*args, **kwargs):
        instance = self._instance
        Item = instance._fields[self._name].field.document_type_obj
        item = Item(**kwargs)
        self.append(item)
        instance.save()
        return item
    return inner


def update_item(item, new_values):
    if not isinstance(new_values, dict):
        return
    for k, v in new_values.items():
        setattr(item, k, v)


def _update(self):
    def inner(new_values, **kwargs):
        values = only_matches(self, kwargs)
        for item in values:
            update_item(item, new_values)
        self._instance.save()
        self._instance.reload()
        if len(values) > 1:
            return FilteredList(values,
                                getinstance(self._instance),
                                self._name)
        else:
            return values and values[0]
    return inner


def _count(self):
    def inner(*args, **kwargs):
        return len(self)
    return inner


def inject(obj):
    setattr(obj, 'filter', _filter(obj))
    setattr(obj, 'get', _get(obj))
    setattr(obj, 'delete', _delete(obj))
    setattr(obj, 'create', _create(obj))
    setattr(obj, 'exclude', _exclude(obj))
    setattr(obj, 'count', _count(obj))
    setattr(obj, 'update', _update(obj))


class FilteredList(BaseList):
    def __init__(self, *args, **kwargs):
        super(FilteredList, self).__init__(*args, **kwargs)
        inject(self)


class ListField(fields.ListField):
    def __get__(self, *args, **kwargs):
        value = super(ListField, self).__get__(*args, **kwargs)
        inject(value)
        return value
