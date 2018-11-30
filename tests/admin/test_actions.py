import pytest
import mock
import json
import random
from copy import deepcopy
from datetime import datetime
from flask import Response, current_app, flash, redirect, url_for, Markup
from flask_admin.actions import action
from quokka.utils.text import slugify
from quokka.admin.actions import PublishAction, CloneAction, UserProfileBlockAction, ExportAction
from quokka.core.app import QuokkaApp
from quokka.core.flask_dynaconf import configure_dynaconf

##################################################
#pytest - Quokka - quokka/admin/test_actions.py  #
##################################################
def test_publishaction_class_instance_of():
    pa = PublishAction()
    assert isinstance(pa, PublishAction) == True

def test_cloneaction_class_instance_of():
    ca = CloneAction()             
    assert isinstance(ca, CloneAction) == True    

def test_userprofileblockaction_class_instance_of():
    upba = UserProfileBlockAction()
    assert isinstance(upba, UserProfileBlockAction) == True    

def test_exportaction_class_instance_of():
    ea = ExportAction()              
    assert isinstance(ea, ExportAction) == True    
    
def test_publishaction_class_def_action_toggle_publish_method_instance_error_outside_context():
    with pytest.raises(RuntimeError) as err:
        pa = PublishAction()              
        pa.action_toggle_publish('12345')
        assert "Working outside of application context." in str(err.value)

def test_cloneaction_class_def_action_clone_item_method_instance_error_outside_context():
    with pytest.raises(RuntimeError) as err:
        ca = CloneAction()              
        ca.action_clone_item('12345')
        assert "Working outside of application context." in str(err.value)

def test_userprofileblockaction_class_def_action_create_userprofile_method_instance_error_outside_context():
    with pytest.raises(RuntimeError) as err:
        upba = UserProfileBlockAction()              
        upba.action_create_userprofile('12345')
        assert "Working outside of application context." in str(err.value)

def test_exportaction_class_def_export_to_json_method_instance_error_outside_context():
    with pytest.raises(AttributeError) as err:
        ea = ExportAction()              
        ea.export_to_json('12345')
        assert "object has no attribute" in str(err.value)

def test_exportaction_class_def_export_to_csv_method_instance_error_outside_context():
    with pytest.raises(AttributeError) as err:
        ea = ExportAction()              
        ea.export_to_csv('12345')
        assert "object has no attribute" in str(err.value)

