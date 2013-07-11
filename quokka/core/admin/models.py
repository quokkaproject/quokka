# coding : utf -8


from flask.ext.security import current_user


class Roled(object):

    def is_accessible(self):

        roles_accepted = getattr(self, 'roles_accepted', None)
        if roles_accepted:
            accessible = any(
                [current_user.has_role(role) for role in roles_accepted]
            )
            return accessible
        return True
