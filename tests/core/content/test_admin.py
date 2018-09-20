import mock
import pytest
import datetime as dt
import pymongo
from flask import current_app
from quokka.admin.forms import ValidationError, rules
from quokka.admin.views import ModelView
from quokka.admin.formatters import (
    format_datetime, format_view_on_site, format_custom_vars
)
from quokka.core.auth import get_current_user
from quokka.utils.text import slugify, slugify_category
from quokka.core.content.formats import CreateForm, get_format
from quokka.core.content.utils import url_for_content
from quokka.core.content.admin import AdminContentView, AdminArticlesView, AdminPagesView, AdminBlocksView


#WIP:
"""
(.venv) [marcosptf@localhost quokka]$ python3.6
Python 3.6.1 (default, May 15 2017, 11:42:04) 
[GCC 6.3.1 20161221 (Red Hat 6.3.1-1)] on linux
Type "help", "copyright", "credits" or "license" for more information.
>> import mock
>>> import pytest
>>> import datetime as dt
>>> import pymongo
>>> from flask import current_app
>>> from quokka.admin.forms import ValidationError, rules
>>> from quokka.admin.views import ModelView
>>> from quokka.admin.formatters import (
...     format_datetime, format_view_on_site, format_custom_vars
... )
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/marcosptf/developer/quokka/quokka/admin/formatters.py", line 3, in <module>
    from quokka.core.content.models import make_model
  File "/home/marcosptf/developer/quokka/quokka/core/content/__init__.py", line 2, in <module>
    from .admin import AdminArticlesView, AdminPagesView, AdminBlocksView
  File "/home/marcosptf/developer/quokka/quokka/core/content/admin.py", line 7, in <module>
    from quokka.admin.formatters import (
ImportError: cannot import name 'format_datetime'
>>> from quokka.core.auth import get_current_user
>>> from quokka.utils.text import slugify, slugify_category
>>> from quokka.core.content.formats import CreateForm, get_format
>>> from quokka.core.content.utils import url_for_content
>>> from quokka.core.content.admin import AdminContentView, AdminArticlesView, AdminPagesView, AdminBlocksView
>>> 
>>> 
>>> acv = AdminContentView(ModelView)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/marcosptf/developer/quokka/.venv/lib64/python3.6/site-packages/flask_admin/contrib/pymongo/view.py", line 97, in __init__
    name = self._prettify_name(coll.name)
AttributeError: type object 'ModelView' has no attribute 'name'
>>> 
>>> mv = ModelView()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: __init__() missing 1 required positional argument: 'coll'
>>> mv = ModelView('mock-coll')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/marcosptf/developer/quokka/.venv/lib64/python3.6/site-packages/flask_admin/contrib/pymongo/view.py", line 97, in __init__
    name = self._prettify_name(coll.name)
AttributeError: 'str' object has no attribute 'name'
>>> param = {'name' : 'mock-name'}
>>> print(param)
{'name': 'mock-name'}
>>> print(param.name)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'dict' object has no attribute 'name'
>>> print(param['name'])
mock-name
>>> class ParamModelViewMock():
...     def name():
...         return "param-mock"
... 
>>> 
>>> pmvm = ParamModelViewMock()
>>> 
>>> mv = ModelView(pmvm)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/marcosptf/developer/quokka/.venv/lib64/python3.6/site-packages/flask_admin/contrib/pymongo/view.py", line 97, in __init__
    name = self._prettify_name(coll.name)
  File "/home/marcosptf/developer/quokka/.venv/lib64/python3.6/site-packages/flask_admin/model/base.py", line 1646, in _prettify_name
    return prettify_name(name)
  File "/home/marcosptf/developer/quokka/.venv/lib64/python3.6/site-packages/flask_admin/model/helpers.py", line 10, in prettify_name
    return name.replace('_', ' ').title()
AttributeError: 'function' object has no attribute 'replace'
>>> 
>>> 

"""
def test_AdminContentView():
    pass

def test_AdminArticlesView():
    pass

def test_AdminPagesView():
    pass

def test_AdminBlocksView():
    pass


