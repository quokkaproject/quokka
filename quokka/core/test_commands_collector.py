from mock import patch
from quokka.core.tests import BaseTestCase
from quokka.ext.commands_collector import CommandsCollector


class TestCommandsCollector(BaseTestCase):

    @patch('quokka.ext.commands_collector.os.walk')
    @patch('quokka.ext.commands_collector.os.listdir')
    @patch('quokka.ext.commands_collector.importlib.import_module')
    def test_load_commands(self, m_import_module, m_listdir, m_walk):
        m_walk.return_value = [('px', ['commands', 'aaa'], 'aa')]
        m_listdir.return_value = [
            'cmd_testx.py', 'cmd_blah', 'a.py', 'cmd_xyz.py']
        cmd = CommandsCollector('my_path', 'my_module')
        self.assertIn('testx', cmd.commands)
        self.assertListEqual(['testx', 'xyz'], cmd.list_commands(cmd))

        cmd.get_command(cmd, 'testx')
        m_import_module.assert_called_once_with(
            'my_module.px.commands.cmd_testx')
