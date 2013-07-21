#!/usr/bin/env python
#coding: utf-8

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
    strict_text = map(lambda x: x if x in permitted_chars else '', ascii_text)
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
