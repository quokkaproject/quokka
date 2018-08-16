import pytest
import mock
from flask_admin import form
from flask_admin.form.upload import ImageUploadInput
from quokka.admin.fields import SmartSelect2Field, ThumbWidget, ThumbField, ContentImageField


def test_SmartSelect2Field_class_assert_creation_counter_property():
    ss2f = SmartSelect2Field()
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
            ss2f = SmartSelect2Field()
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




