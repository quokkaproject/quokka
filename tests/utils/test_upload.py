import pytest
import mock
import os.path as op
import random
from datetime import date
from flask import current_app
from speaklater import make_lazy_string
from werkzeug import secure_filename
from quokka.utils.upload import (
    dated_path, media_path,
    lazy_media_path
)


################################
#pytest - fixtures - setUp();  #
################################
class MockClassParam():
    model_name = None
    def __init__(self):
        self.model_name = "model-name-mock"

class MockClassFileParam():
    filename = None
    def __init__(self):
        self.filename = "file_name-mock"

mock_class_param = MockClassParam()
mock_class_file_param = MockClassFileParam()
dated = dated_path(mock_class_param, file_data=mock_class_file_param)


##################################
#pytest - Quokka - test_text.py  #
##################################
def test_dated_path():
    assert 'model-name-mock' in dated

def media_path():
    with pytest.raises(RuntimeError) as err:
        media_path(suffix=None)
        assert "Working outside of application context." in str(err.value)
