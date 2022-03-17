import logging
import time
from threading import Thread
from typing import Final

import RPi.GPIO as GPIO

from config_file import ConfigFile
from util import swap_config


class SwitchDisplay(Thread):
    def __init__(self,
                 config_current: ConfigFile,
                 config_lcd: ConfigFile,
                 config_hdmi: ConfigFile,
                 reboot: bool = False,
                 hdmi_hdp_pin: int = 18,
                 sleep_seconds: int = 1
                 ):
        super().__init__()
        self._hdmi_hdp_pin: Final = hdmi_hdp_pin
        self._config_current: Final = config_current
        self._config_lcd: Final = config_lcd
        self._config_hdmi: Final = config_hdmi
        self._reboot: Final = reboot
        self._sleep_seconds: Final = sleep_seconds
        self._log = logging.getLogger(__name__)

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._hdmi_hdp_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def run(self):
        time.sleep(self._sleep_seconds)

        if GPIO.input(self._hdmi_hdp_pin) == GPIO.HIGH:
            self._log.info(f'Currently connected to HDMI, pin "{self._hdmi_hdp_pin}" is HIGH.')
            if self._config_current != self._config_hdmi:
                swap_config(self._config_hdmi, self._config_current, reboot=self._reboot)
                return

            self._log.info(f'Waiting for HDMI disconnect now.')
            GPIO.wait_for_edge(self._hdmi_hdp_pin, GPIO.FALLING)
            swap_config(self._config_lcd, self._config_current, reboot=self._reboot)

        elif GPIO.input(self._hdmi_hdp_pin) == GPIO.LOW:
            self._log.info(f'Currently connected to LCD, pin "{self._hdmi_hdp_pin}" is LOW.')
            if self._config_current != self._config_lcd:
                swap_config(self._config_lcd, self._config_current, reboot=self._reboot)
                return

            self._log.info(f'Waiting for HDMI connect now.')
            GPIO.wait_for_edge(self._hdmi_hdp_pin, GPIO.RISING)
            swap_config(self._config_hdmi, self._config_current, reboot=self._reboot)
