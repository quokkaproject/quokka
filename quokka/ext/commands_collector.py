import sys
import os
import click
import importlib


class CommandsCollector(click.MultiCommand):
    """A MultiCommand to collect all click commands from a given
    modules path and base name for the module.
    The commands functions needs to be in a commands folder and
    the name needs to start with the prefix 'cmd_' followed by
    the command name.
    """

    def __init__(self, modules_path, base_module_name, **attrs):
        click.MultiCommand.__init__(self, **attrs)
        self.base_module_name = base_module_name
        self.commands = {}
        self.load_commands(modules_path)

    def load_commands(self, modules_path):
        for _path, _dir, _files in os.walk(modules_path):
            if 'commands' not in _dir:
                continue
            for filename in os.listdir(os.path.join(_path, 'commands')):
                if filename.endswith('.py') and filename.startswith('cmd_'):
                    cmd = filename[4:-3]
                    _, self.commands[cmd] = os.path.split(_path)

    def list_commands(self, ctx):
        rv = self.commands.keys()
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        try:
            if sys.version_info[0] == 2:
                name = name.encode('ascii', 'replace')
            module_name = '{}.{}.commands.cmd_{}'.format(
                self.base_module_name,
                self.commands[name],
                name)
            mod = importlib.import_module(module_name)
        except ImportError:
            return
        return mod.cli
