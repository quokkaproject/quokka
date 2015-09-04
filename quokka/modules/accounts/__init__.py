# coding: utf8
from quokka.core.app import QuokkaModule
from .views import SwatchView


module = QuokkaModule('accounts', __name__, template_folder='templates')
module.add_url_rule('/set_swatch/',
                    view_func=SwatchView.as_view('set_swatch'))
