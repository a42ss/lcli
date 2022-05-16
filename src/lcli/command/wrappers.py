from lcli.app import App
from lcli.command.subprocess import CommandRunner
from lcli.command.input import ParametersReader
from lcli.tools.base import BaseTool
from lcli.config import *
from lcli.command.builders import BaseBuilder


class BaseCommandWrapperInterface(object):
    pass


class BashCommandWrapperInterface(BaseCommandWrapperInterface):
    pass


class BashCommandWrapper(BaseTool, BashCommandWrapperInterface):
    """
    Run command from configuration, commands with type wrapper
    This will consist of executing shell commands on a given directory using configuration, parameters completion and
    interactive selections of parameters
    """
    _command_name: str
    _command: Command

    def __init__(self, app: App, command: Command) -> None:
        super().__init__(app)
        self._command_name = command.name
        self._command = command
        self.__init_command()

    def __init_command(self):
        self.__doc__ = self._command.description

        sub_commands = self._command.commands
        for command_code in sub_commands:
            current_command = sub_commands[command_code]
            current_command_obj = CommandRunner(
                current_command,
                self._app.get_config_object().get(['commands_defaults', self._command_name], default={}),
                self._app.get_object_manager().provide(ParametersReader.Factory),
                self._command
            )
            current_command_obj.__doc__ = current_command.description + " (" + current_command.args.command + ")"
            setattr(self, command_code, current_command_obj)

    class _Builder(BaseBuilder):
        """
        This will be a custom builder for current wrapper, custom ones may be implemented
        """

        def build(self, command: Command) -> 'BashCommandWrapper':
            return BashCommandWrapper(self._app, command)


class ManualWrapper(dict):
    pass
