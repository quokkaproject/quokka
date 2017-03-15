#!/usr/bin/env python
# coding: utf-8

"""
This functions created by Alvaro Justen (Turicas)
"""
from slugify import slugify as awesome_slugify


def slugify(text):
    return awesome_slugify(text).lower()


def abbreviate(name, pretty=False):
    names = name.split()
    if len(names) == 1:
        return name
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
