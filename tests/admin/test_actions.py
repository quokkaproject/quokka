import pytest
import mock
import json
import random
from copy import deepcopy
from datetime import datetime
from flask import Markup
from flask import Response, current_app, flash, redirect, url_for
from flask_admin.actions import action
from quokka.utils.text import slugify
from quokka.admin.actions import PublishAction

#pytest: WIP
def test_PublishAction_class_def_action_toggle_publish_method_instance():
    pass
#>>> pa = PublishAction()                          
#>>> type(pa)
#<class 'quokka.admin.actions.PublishAction'>
#>>> print(pa)
#<quokka.admin.actions.PublishAction object at 0x7fcf203936d8>
#>>> print(pa)                      
#<quokka.admin.actions.PublishAction object at 0x7fcf203936d8>
#>>> print(pa.action_toggle_publish('1234'))
#Traceback (most recent call last):
  #File "<stdin>", line 1, in <module>
  #File "/home/marcosptf/developer/quokka/quokka/admin/actions.py", line 22, in action_toggle_publish
    #model = current_app.db.get_with_content(_id=_id)
  #File "/home/marcosptf/developer/quokka/.venv/lib64/python3.6/site-packages/werkzeug/local.py", line 347, in __getattr__
    #return getattr(self._get_current_object(), name)
  #File "/home/marcosptf/developer/quokka/.venv/lib64/python3.6/site-packages/werkzeug/local.py", line 306, in _get_current_object
    #return self.__local()
  #File "/home/marcosptf/developer/quokka/.venv/lib64/python3.6/site-packages/flask/globals.py", line 51, in _find_app
    #raise RuntimeError(_app_ctx_err_msg)
#RuntimeError: Working outside of application context.

#This typically means that you attempted to use functionality that needed
#to interface with the current application object in some way. To solve
#this, set up an application context with app.app_context().  See the
#documentation for more information.
#>>> 
