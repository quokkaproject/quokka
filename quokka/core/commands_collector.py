import importlib
import os
import sys

import click


class CommandsCollector(click.MultiCommand):
    """A MultiCommand to collect all click commands from a given
    modules path and base name for the module.
    The commands functions needs to be in a module inside commands
    folder and the name of the file will be used as the command name.
    """

    def __init__(self, modules_path, base_module_name, **attrs):
        click.MultiCommand.__init__(self, **attrs)
        self.base_module_name = base_module_name
        self.modules_path = modules_path

    def list_commands(self, *args, **kwargs):
        commands = []
        for _path, _dir, _ in os.walk(self.modules_path):
            if 'commands' not in _dir:
                continue
            for filename in os.listdir(os.path.join(_path, 'commands')):
                if filename.endswith('.py') and filename != '__init__.py':
                    cmd = filename[:-3]
                    _, module_name = os.path.split(_path)
                    commands.append('{0}_{1}'.format(module_name, cmd))
        commands.sort()
        return commands

    def get_command(self, ctx, name):
        try:
            if sys.version_info[0] == 2:
                name = name.encode('ascii', 'replace')
            splitted = name.split('_')
            if len(splitted) <= 1:
                return
            module_name, command_name = splitted
            if not all([module_name, command_name]):
                return
            module = '{0}.{1}.commands.{2}'.format(
                self.base_module_name,
                module_name,
                command_name)
            mod = importlib.import_module(module)
        except ImportError:
            return
        return getattr(mod, 'cli', None)
