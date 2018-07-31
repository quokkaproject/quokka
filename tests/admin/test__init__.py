import mock
import quokka
from quokka.admin.views import FileAdmin, IndexView, ModelView
from quokka.admin import create_admin, QuokkaAdmin

@mock.patch("quokka.admin.views.IndexView")
@mock.patch("quokka.admin.QuokkaAdmin")
def test_create_admin(mock_QuokkaAdmin, mock_IndexView):
    import yaml
    stream = open("quokka/project_template/quokka.yml")
    docs = yaml.load_all(stream)
    quokka.admin.create_admin(app=docs)
    assert mock_IndexView.called is False

