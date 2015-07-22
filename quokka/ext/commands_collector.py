import sys
import os
import click
import importlib


class CommandsCollector(click.MultiCommand):

    def __init__(self, search_path, **attrs):
        click.MultiCommand.__init__(self, **attrs)
        self.search_path = search_path
        self.commands_module = {}

    def list_commands(self, ctx):
        rv = []
        for _path, _dir, _files in os.walk(self.search_path):
            if 'commands' not in _dir:
                continue
            for filename in os.listdir(os.path.join(_path, 'commands')):
                if filename.endswith('.py') and filename.startswith('cmd_'):
                    cmd = filename[4:-3]
                    rv.append(cmd)
                    _, self.commands_module[cmd] = os.path.split(_path)
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        try:
            if sys.version_info[0] == 2:
                name = name.encode('ascii', 'replace')
            module_name = 'quokka.modules.{}.commands.cmd_{}'.format(
                self.commands_module[name],
                name)
            mod = importlib.import_module(module_name)
        except ImportError:
            return
        return mod.cli
