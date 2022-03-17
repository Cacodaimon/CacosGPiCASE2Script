import logging
from os import system
from typing import Final

from config_file import ConfigFile
from util import copy_resource_to_file
from util import shutdown


class CopyConfigFiles:
    def __init__(self,
                 config_current: ConfigFile,
                 config_lcd: ConfigFile,
                 config_hdmi: ConfigFile,
                 ):

        self._config_current: Final = config_current
        self._config_lcd: Final = config_lcd
        self._config_hdmi: Final = config_hdmi
        self._log = logging.getLogger(__name__)

    def ensure_config_files_exists(self):
        if self._config_lcd.exists and self._config_hdmi.exists:
            self._log.info(f'Check all config files already exist.')

            return

        self._log.info(f'Some config files are missing.')
        system('mount -o remount, rw /boot')
        for config in [self._config_lcd, self._config_hdmi]:
            copy_resource_to_file(f'configs/{config.base_name}', config.file_name)
