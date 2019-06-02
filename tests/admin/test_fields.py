import pytest
import mock
from flask_admin import form
from flask_admin.form.upload import ImageUploadInput
from quokka.admin.fields import SmartSelect2Field, ThumbWidget, ThumbField, ContentImageField

################################
#pytest - fixtures - setUp();  #
################################
ss2f = SmartSelect2Field()
tw = ThumbWidget()
tf = ThumbField()
cif = ContentImageField()

##################################################
#pytest - Quokka - quokka/admin/test_fields.py  #
##################################################
def test_smartselect2field_isinstance_of_false():
    assert isinstance(ss2f, SmartSelect2Field) == False

def test_thumbwidget_isinstance_of():
    assert isinstance(tw, ThumbWidget) == True

def test_thumbfield_isinstance_of_false():
    assert isinstance(tf, ThumbField) == False

def test_contentimagefield_isinstance_of_false():
    assert isinstance(cif, ContentImageField) == False
    
def test_smartselect2field_class_assert_creation_counter_property():
    assert ss2f.creation_counter == 7
    
def test_smartselect2field_class_assert_iter_choices_method():
    with pytest.raises(AttributeError) as err:
        ss2f = SmartSelect2Field()
        ss2f.iter_choices()
        assert "object has no attribute" in str(err.value)
    
def test_smartselect2field_class_assert_concrete_choices_method():
    with pytest.raises(AttributeError) as err:
        ss2f = SmartSelect2Field()
        ss2f.concrete_choices()
        assert "object has no attribute" in str(err.value)
    
def test_smartselect2field_class_assert_concrete_choices_property():
    with pytest.raises(AttributeError) as err:
        ss2f = SmartSelect2Field()
        ss2f.concrete_choices
        assert "object has no attribute" in str(err.value)
    
def test_smartselect2field_class_assert_choice_values_method():
    with pytest.raises(AttributeError) as err:
        ss2f = SmartSelect2Field()
        ss2f.choice_values()
        assert "object has no attribute" in str(err.value)
   
def test_smartselect2field_class_assert_choice_values_property():
    with pytest.raises(AttributeError) as err:
        ss2f = SmartSelect2Field()
        ss2f.choice_values
        assert "object has no attribute" in str(err.value)

def test_smartselect2field_class_assert_pre_validate_method():
    with pytest.raises(AttributeError) as err:
        ss2f.pre_validate()
        assert "object has no attribute" in str(err.value)

def test_thumbwidget_data_template_property():
    assert tw.data_template == '<div class="image-thumbnail"> <img %(image)s></div>'

def test_thumbwidget_empty_template_property():
    assert tw.empty_template == ''

def test_thumbfield_get_args_empty():
    assert tf.args == ()

def test_thumbfield_get_kwargs_empty():
    assert tf.kwargs == {}

def test_thumbfield_creation_counter_property():
    assert tf.creation_counter == 8

def test_contentimagefield_get_args_property():
    assert cif.args == ()

def test_contentimagefield_get_kwargs_property():
    assert cif.kwargs == {}
    
def test_contentimagefield_get_kwargs_property():
    assert cif.creation_counter == 9

