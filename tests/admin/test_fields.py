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
def test_SmartSelect2Field_isinstance_of_False():
    assert isinstance(ss2f, SmartSelect2Field) == False

def test_ThumbWidget_isinstance_of():
    assert isinstance(tw, ThumbWidget) == True

def test_ThumbField_isinstance_of_False():
    assert isinstance(tf, ThumbField) == False

def test_ContentImageField_isinstance_of_False():
    assert isinstance(cif, ContentImageField) == False
    
def test_SmartSelect2Field_class_assert_creation_counter_property():
    assert ss2f.creation_counter == 7
    
def test_SmartSelect2Field_class_assert_iter_choices_method():
    with pytest.raises(AttributeError) as err:
        try:
            ss2f = SmartSelect2Field()
            ss2f.iter_choices()
            assert "object has no attribute" in str(err.value)

        except TypeError as e:
            assert 'nargs=-1' in str(e)

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        except FileExistsError:
            raise        

        except Exception:
            raise

    
def test_SmartSelect2Field_class_assert_concrete_choices_method():
    with pytest.raises(AttributeError) as err:
        try:
            ss2f = SmartSelect2Field()
            ss2f.concrete_choices()
            assert "object has no attribute" in str(err.value)

        except TypeError as e:
            assert 'nargs=-1' in str(e)

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        except FileExistsError:
            raise        

        except Exception:
            raise

    
def test_SmartSelect2Field_class_assert_concrete_choices_property():
    with pytest.raises(AttributeError) as err:
        try:
            ss2f = SmartSelect2Field()
            ss2f.concrete_choices
            assert "object has no attribute" in str(err.value)

        except TypeError as e:
            assert 'nargs=-1' in str(e)

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        except FileExistsError:
            raise        

        except Exception:
            raise

    
def test_SmartSelect2Field_class_assert_choice_values_method():
    with pytest.raises(AttributeError) as err:
        try:
            ss2f = SmartSelect2Field()
            ss2f.choice_values()
            assert "object has no attribute" in str(err.value)

        except TypeError as e:
            assert 'nargs=-1' in str(e)

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        except FileExistsError:
            raise        

        except Exception:
            raise

    
def test_SmartSelect2Field_class_assert_choice_values_property():
    with pytest.raises(AttributeError) as err:
        try:
            ss2f = SmartSelect2Field()
            ss2f.choice_values
            assert "object has no attribute" in str(err.value)

        except TypeError as e:
            assert 'nargs=-1' in str(e)

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        except FileExistsError:
            raise        

        except Exception:
            raise


def test_SmartSelect2Field_class_assert_pre_validate_method():
    with pytest.raises(AttributeError) as err:
        try:
            ss2f.pre_validate()
            assert "object has no attribute" in str(err.value)

        except TypeError as e:
            assert 'nargs=-1' in str(e)

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        except FileExistsError:
            raise        

        except Exception:
            raise


def test_ThumbWidget_data_template_property():
    assert tw.data_template == '<div class="image-thumbnail"> <img %(image)s></div>'

def test_ThumbWidget_empty_template_property():
    assert tw.empty_template == ''

def test_ThumbField_get_args_empty():
    assert tf.args == ()

def test_ThumbField_get_kwargs_empty():
    assert tf.kwargs == {}

def test_ThumbField_creation_counter_property():
    assert tf.creation_counter == 8

def test_ContentImageField_get_args_property():
    assert cif.args == ()

def test_ContentImageField_get_kwargs_property():
    assert cif.kwargs == {}
    
def test_ContentImageField_get_kwargs_property():
    assert cif.creation_counter == 9

