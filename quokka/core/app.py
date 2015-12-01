from flask import Flask, Blueprint
from quokka.core.config import QuokkaConfig
from quokka.utils.aliases import dispatch_aliases


class QuokkaApp(Flask):
    """
    Implementes customizations on Flask
    - Config handler
    - Aliases dispatching before request
    """

    config_class = QuokkaConfig

    def make_config(self, instance_relative=False):
        """This method should be removed when Flask is >=0.11"""
        root_path = self.root_path
        if instance_relative:
            root_path = self.instance_path
        return self.config_class(root_path, self.default_config)

    def preprocess_request(self):
        return dispatch_aliases() or super(QuokkaApp,
                                           self).preprocess_request()


class QuokkaModule(Blueprint):
    "for future overriding"
