# coding: utf-8

from dynaconf.utils.parse_conf import parse_conf_data


def parse_data(data):
    """Return converted data from @int, @float, @bool, @json markers"""
    return parse_conf_data(data)


def custom_var_dict(cvarlist):
    cvarlist = cvarlist or []
    return {
        cvar['key']: parse_data(cvar['value'])
        for cvar in cvarlist
    }
