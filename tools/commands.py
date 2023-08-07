# This file is part of the EESSI build-and-deploy bot,
# see https://github.com/EESSI/eessi-bot-software-layer
#
# The bot helps with requests to add software installations to the
# EESSI software layer, see https://github.com/EESSI/software-layer
#
# author: Thomas Roeblitz (@trz42)
#
# license: GPLv2
#

# Standard library imports
import re
import sys

# Third party imports (anything installed into the local Python environment)
from pyghee.utils import log

# Local application imports (anything from EESSI/eessi-bot-software-layer)
from tools.filter import EESSIBotActionFilter, EESSIBotActionFilterError


def get_bot_command(line):
    """
        Retrieve bot command from a line.
    Args:
        line (string): string that is scanned for a command

    Returns:
        command (string): the command if any found or None
    """
    fn = sys._getframe().f_code.co_name

    log(f"{fn}(): searching for bot command in '{line}'")
    match = re.search('^bot: (.*)$', line)
    if match:
        return match.group(1).rstrip()
    else:
        return None


class EESSIBotCommandError(Exception):
    pass


class EESSIBotCommand:
    """
    Class for representing a bot command which includes the command itself and
    a filter to limit for which architecture, repository and bot instance the
    command should be applied to.
    """
    def __init__(self, cmd_str):
        cmd_as_list = cmd_str.split()
        self.command = cmd_as_list[0]
        if len(cmd_as_list) > 1:
            arg_str = " ".join(cmd_as_list[1:])
            try:
                self.action_filters = EESSIBotActionFilter(arg_str)
            except EESSIBotActionFilterError as err:
                log(f"ERROR: EESSIBotActionFilterError - {err.args}")
                self.action_filters = None
                raise EESSIBotCommandError("invalid action filter")
            except Exception as err:
                log(f"Unexpected err={err}, type(err)={type(err)}")
                raise
        else:
            self.action_filters = EESSIBotActionFilter("")

    def to_string(self):
        action_filters_str = self.action_filters.to_string()
        return f"{' '.join([self.command, action_filters_str]).rstrip()}"
