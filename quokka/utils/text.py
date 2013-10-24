#!/usr/bin/env python
# coding: utf-8

"""
This functions created by Alvaro Justen (Turicas)
"""
from unicodedata import normalize


def slugify(text, encoding=None,
            permitted_chars='abcdefghijklmnopqrstuvwxyz0123456789-'):
    if isinstance(text, str):
        text = text.decode(encoding or 'ascii')
    clean_text = text.strip().replace(' ', '-').lower()
    while '--' in clean_text:
        clean_text = clean_text.replace('--', '-')
    ascii_text = normalize('NFKD', clean_text).encode('ascii', 'ignore')
    strict_text = [x if x in permitted_chars else '' for x in ascii_text]
    return ''.join(strict_text)


def abbreviate(name, pretty=False):
    names = name.split()
    if len(names) == 2:
        return name
    result = [names[0]]
    tiny_name = False
    for surname in names[1:-1]:
        if len(surname) <= 3:
            result.append(surname)
            tiny_name = True
        else:
            if pretty and tiny_name:
                result.append(surname)
            else:
                result.append(surname[0] + '.')
            tiny_name = False
    result.append(names[-1])
    return ' '.join(result)


class LazyString(str):
    def __init__(self, func):
        self.func = func
        self.value = None
        self._decoded = None

    @property
    def decoded(self):
        if self._decoded is None:
            self._decoded = self.func()
        return self._decoded

    def __repr__(self):
        return self.decoded

    def __str__(self):
        return str(self.decoded)

    def __unicode__(self):
        return unicode(self.decoded)

    def __len__(self):
        return len(self.decoded)

    def __getitem__(self, i):
        return self.decoded.__getitem__(i)

    def __getslice__(self, i, j):
        return self.decoded.__getslice__(i, j)

    def encode(self, *args, **kwargs):
        return self.decoded.encode(*args, **kwargs)

    def decode(self, *args, **kwargs):
        return self.decoded.decode(*args, **kwargs)

    def split(self, *args, **kwargs):
        return self.decoded.split(*args, **kwargs)

    def rsplit(self, *args, **kwargs):
        return self.decoded.rsplit(*args, **kwargs)

    def lsplit(self, *args, **kwargs):
        return self.decoded.lsplit(*args, **kwargs)

    def lower(self, *args, **kwargs):
        return self.decoded.lower(*args, **kwargs)

    def upper(self, *args, **kwargs):
        return self.decoded.upper(*args, **kwargs)

    def capitalize(self, *args, **kwargs):
        return self.decoded.capitalize(*args, **kwargs)

    def center(self, *args, **kwargs):
        return self.decoded.center(*args, **kwargs)

    def count(self, *args, **kwargs):
        return self.decoded.count(*args, **kwargs)

    def endswith(self, *args, **kwargs):
        return self.decoded.endswith(*args, **kwargs)

    def startswith(self, *args, **kwargs):
        return self.decoded.startswith(*args, **kwargs)

    def expandtabs(self, *args, **kwargs):
        return self.decoded.expandtabs(*args, **kwargs)

    def find(self, *args, **kwargs):
        return self.decoded.find(*args, **kwargs)

    def format(self, *args, **kwargs):
        return self.decoded.format(*args, **kwargs)

    def index(self, *args, **kwargs):
        return self.decoded.index(*args, **kwargs)

    def join(self, *args, **kwargs):
        return self.decoded.join(*args, **kwargs)

    def ljust(self, *args, **kwargs):
        return self.decoded.ljust(*args, **kwargs)

    def strip(self, *args, **kwargs):
        return self.decoded.strip(*args, **kwargs)

    def partition(self, *args, **kwargs):
        return self.decoded.partition(*args, **kwargs)

    def replace(self, *args, **kwargs):
        return self.decoded.replace(*args, **kwargs)

    def rfind(self, *args, **kwargs):
        return self.decoded.rfind(*args, **kwargs)

    def rindex(self, *args, **kwargs):
        return self.decoded.rindex(*args, **kwargs)

    def lstrip(self, *args, **kwargs):
        return self.decoded.lstrip(*args, **kwargs)

    def rstrip(self, *args, **kwargs):
        return self.decoded.rsplit(*args, **kwargs)

    def translate(self, *args, **kwargs):
        return self.decoded.translate(*args, **kwargs)

    def splitlines(self, *args, **kwargs):
        return self.decoded.splitlines(*args, **kwargs)

    def __add__(self, *args, **kwargs):
        return self.decoded.__add__(*args, **kwargs)

    def __eq__(self, *args, **kwargs):
        return self.decoded.__eq__(*args, **kwargs)

    def __ne__(self, *args, **kwargs):
        return self.decoded.__ne__(*args, **kwargs)

    def __reduce__(self, *args, **kwargs):
        return self.decoded.__reduce__(*args, **kwargs)


if __name__ == '__main__':
    print((slugify("Selling England by the pound")))
    print((slugify("1234 benção amanhã compro melões é @ $".decode('utf8'))))
