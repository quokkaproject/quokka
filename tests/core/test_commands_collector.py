import mock
import click
import importlib
import os
import sys
import click
from quokka.core.commands_collector import CommandsCollector
 

#######################################################
#pytest - fixtures                                    #
#######################################################
command_collector = CommandsCollector(modules_path="quokka/", base_module_name="quokka")


#######################################################
#pytest - Quokka - tests/core/views/test_sitemap.py   #
#######################################################
def test_class_commandscollector_add_help_option():
    assert command_collector.add_help_option == True

def test_class_commandscollector_allow_extra_args():
    assert command_collector.allow_extra_args == True

def test_class_commandscollector_allow_interspersed_args():
    assert command_collector.allow_interspersed_args == False

def test_class_commandscollector_base_module_name():
    assert command_collector.base_module_name == 'quokka'

def test_class_commandscollector_callback():
    assert command_collector.callback is None

def test_class_commandscollector_chain():
    assert command_collector.chain == False

def test_class_commandscollector_context_settings():
    assert command_collector.context_settings == {}

def test_class_commandscollector_epilog():
    assert command_collector.epilog is None

def test_class_commandscollector_help():
    assert command_collector.help is None

def test_class_commandscollector_ignore_unknow_options():
    assert command_collector.ignore_unknown_options == False

def test_class_commandscollector_invoke_without_command():
    assert command_collector.invoke_without_command == False

def test_class_commandscollector_modules_path():
    assert command_collector.modules_path == 'quokka/'

def test_class_commandscollector_name():
    assert command_collector.name is None

def test_class_commandscollector_no_args_is_help():
    assert command_collector.no_args_is_help == True

def test_class_commandscollector_options_metavar():
    assert command_collector.options_metavar == '[OPTIONS]'

def test_class_commandscollector_params():
    assert command_collector.params == []

def test_class_commandscollector_short_help():
    assert command_collector.short_help is None

def test_class_commandscollector_subcommand_metavar():
    assert command_collector.subcommand_metavar == 'COMMAND [ARGS]...'
