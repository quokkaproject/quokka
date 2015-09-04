from flask import Flask, Blueprint
from quokka.core.config import QuokkaConfig


class QuokkaApp(Flask):
    """Implementes a customized config handler"""

    config_class = QuokkaConfig

    def make_config(self, instance_relative=False):
        """This method should be removed when Flask is >=0.11"""
        root_path = self.root_path
        if instance_relative:
            root_path = self.instance_path
        return self.config_class(root_path, self.default_config)


class QuokkaModule(Blueprint):
    "for future overriding"
