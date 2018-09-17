import pytest
import mock
from flask import current_app as app
from flask_htmlbuilder.htmlbuilder import html
from quokka.core.content.models import make_model
from quokka.admin.formatters import format_datetime, \
    format_view_on_site, format_ul, format_link, \
    format_status, format_url, format_custom_vars
from quokka.core.content.models import Content


################################
#pytest - fixtures - setUp();  #
################################
#fm = Formatters()


#####################################################
#pytest - Quokka - quokka/admin/test_formatters.py  #
#####################################################
@mock.patch("quokka.core.content.models.Content")
@mock.patch("quokka.core.content.models.make_model")
def test_format_datetime(mock_make_model, mock_Content):

    with pytest.raises(TypeError) as err:
        try:
            data = {
                'modified' : 'mock-modified',
                'date' : 'mock-date',
                'comments' : 'mock-comments',
                'published' : 'mock-published',
                'language' : 'mock-language',
                'authors' : 'mock-authors',
                'category' : 'mock-category',
                'title' : 'mock-title',
                'name' : 'mock-name',
                '_id' : 'mock-ids',
                'block_items' : 'mock-itens',
                'content_format': 'mock-content'
            }

            content_type = data
            content = mock_Content(data)
            format_datetime(request='', obj=content, fieldname='mock-fieldname')
            assert "arg 2 must be a type or tuple of types" in str(err.value)

        except AttributeError as e:
            assert 'nargs=-1' in str(e)

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
            
        except RuntimeError:
            raise

        except FileExistsError:
            raise    

        except Exception:
            raise



@mock.patch("quokka.core.content.models.Content")
@mock.patch("quokka.core.content.models.make_model")
def test_format_view_on_site(mock_make_model, mock_Content):

    with pytest.raises(TypeError) as err:
        try:
            data = {
                'modified' : 'mock-modified',
                'date' : 'mock-date',
                'comments' : 'mock-comments',
                'published' : 'mock-published',
                'language' : 'mock-language',
                'authors' : 'mock-authors',
                'category' : 'mock-category',
                'title' : 'mock-title',
                'name' : 'mock-name',
                '_id' : 'mock-ids',
                'block_items' : 'mock-itens',
                'content_format': 'mock-content'
            }

            content_type = data
            content = mock_Content(data)
            format_view_on_site(request='', obj=content, fieldname='mock-fieldname')
            assert "arg 2 must be a type or tuple of types" in str(err.value)

        except AttributeError as e:
            assert 'nargs=-1' in str(e)

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        except RuntimeError:
            raise

        except FileExistsError:
            raise

        except Exception:
            raise



@mock.patch("quokka.core.content.models.Content")
@mock.patch("quokka.core.content.models.make_model")
def test_format_ul(mock_make_model, mock_Content):

    with pytest.raises(TypeError) as err:
        try:
            data = {
                'modified' : 'mock-modified',
                'date' : 'mock-date',
                'comments' : 'mock-comments',
                'published' : 'mock-published',
                'language' : 'mock-language',
                'authors' : 'mock-authors',
                'category' : 'mock-category',
                'title' : 'mock-title',
                'name' : 'mock-name',
                '_id' : 'mock-ids',
                'block_items' : 'mock-itens',
                'content_format': 'mock-content'
            }

            content_type = data
            content = mock_Content(data)
            format_ul(request='', obj=content, fieldname='mock-fieldname')
            assert "arg 2 must be a type or tuple of types" in str(err.value)

        except AttributeError as e:
            assert 'nargs=-1' in str(e)

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        except RuntimeError:
            raise

        except FileExistsError:
            raise

        except Exception:
            raise



@mock.patch("quokka.core.content.models.Content")
@mock.patch("quokka.core.content.models.make_model")
def test_format_link(mock_make_model, mock_Content):

    with pytest.raises(TypeError) as err:
        try:
            data = {
                'modified' : 'mock-modified',
                'date' : 'mock-date',
                'comments' : 'mock-comments',
                'published' : 'mock-published',
                'language' : 'mock-language',
                'authors' : 'mock-authors',
                'category' : 'mock-category',
                'title' : 'mock-title',
                'name' : 'mock-name',
                '_id' : 'mock-ids',
                'block_items' : 'mock-itens',
                'content_format': 'mock-content'
            }

            content_type = data
            content = mock_Content(data)
            format_link(request='', obj=content, fieldname='mock-fieldname')
            assert "arg 2 must be a type or tuple of types" in str(err.value)

        except AttributeError as e:
            assert 'nargs=-1' in str(e)

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        except RuntimeError:
            raise

        except FileExistsError:
            raise

        except Exception:
            raise




@mock.patch("quokka.core.content.models.Content")
@mock.patch("quokka.core.content.models.make_model")
def test_format_status(mock_make_model, mock_Content):

    with pytest.raises(TypeError) as err:
        try:
            data = {
                'modified' : 'mock-modified',
                'date' : 'mock-date',
                'comments' : 'mock-comments',
                'published' : 'mock-published',
                'language' : 'mock-language',
                'authors' : 'mock-authors',
                'category' : 'mock-category',
                'title' : 'mock-title',
                'name' : 'mock-name',
                '_id' : 'mock-ids',
                'block_items' : 'mock-itens',
                'content_format': 'mock-content'
            }

            content_type = data
            content = mock_Content(data)
            format_status(request='', obj=content, fieldname='mock-fieldname')
            assert "arg 2 must be a type or tuple of types" in str(err.value)

        except AttributeError as e:
            assert 'nargs=-1' in str(e)

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        except RuntimeError:
            raise

        except FileExistsError:
            raise

        except Exception:
            raise



@mock.patch("quokka.core.content.models.Content")
@mock.patch("quokka.core.content.models.make_model")
def test_format_url(mock_make_model, mock_Content):

    with pytest.raises(TypeError) as err:
        try:
            data = {
                'modified' : 'mock-modified',
                'date' : 'mock-date',
                'comments' : 'mock-comments',
                'published' : 'mock-published',
                'language' : 'mock-language',
                'authors' : 'mock-authors',
                'category' : 'mock-category',
                'title' : 'mock-title',
                'name' : 'mock-name',
                '_id' : 'mock-ids',
                'block_items' : 'mock-itens',
                'content_format': 'mock-content'
            }

            content_type = data
            content = mock_Content(data)
            format_url(request='', obj=content, fieldname='mock-fieldname')
            assert "arg 2 must be a type or tuple of types" in str(err.value)

        except AttributeError as e:
            assert 'nargs=-1' in str(e)

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        except RuntimeError:
            raise

        except FileExistsError:
            raise

        except Exception:
            raise



@mock.patch("quokka.core.content.models.Content")
@mock.patch("quokka.core.content.models.make_model")
def test_format_custom_vars(mock_make_model, mock_Content):

    with pytest.raises(TypeError) as err:
        try:
            data = {
                'modified' : 'mock-modified',
                'date' : 'mock-date',
                'comments' : 'mock-comments',
                'published' : 'mock-published',
                'language' : 'mock-language',
                'authors' : 'mock-authors',
                'category' : 'mock-category',
                'title' : 'mock-title',
                'name' : 'mock-name',
                '_id' : 'mock-ids',
                'block_items' : 'mock-itens',
                'content_format': 'mock-content',
                'custom_vars' : 'mock-custom-vars',
                'value' : 'mock-value'
            }

            content_type = data
            content = mock_Content(data)
            format_custom_vars(request='', obj=data, fieldname='mock-fieldname')
            assert "arg 2 must be a type or tuple of types" in str(err.value)

        except AttributeError as e:
            assert 'nargs=-1' in str(e)

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        except RuntimeError:
            raise

        except FileExistsError:
            raise

        except Exception:
            raise






