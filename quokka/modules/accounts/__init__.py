# coding: utf8
from quokka.core.app import QuokkaModule
from .views import SwatchView, ProfileEditView, ProfileView


module = QuokkaModule('accounts', __name__, template_folder='templates')
module.add_url_rule('/accounts/set_swatch/',
                    view_func=SwatchView.as_view('set_swatch'))
module.add_url_rule('/accounts/profile/<user_id>/',
                    view_func=ProfileView.as_view('profile'))
module.add_url_rule('/accounts/profile/edit/',
                    view_func=ProfileEditView.as_view('profile_edit'))
