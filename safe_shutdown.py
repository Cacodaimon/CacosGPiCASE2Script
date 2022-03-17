import logging
from typing import Final

import RPi.GPIO as GPIO

from util import shutdown


class SafeShutdown:
    def __init__(self,
                 power_pin: int = 26,
                 power_en_pin: int = 27,
                 ):
        super().__init__()
        self._log = logging.getLogger(__name__)

        self._log.info(f'Configuring GPIO pin "{power_pin}" and "{power_en_pin}".')
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(power_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(power_en_pin, GPIO.OUT)
        GPIO.output(power_en_pin, GPIO.HIGH)
        self._log.info(f'GPIO pin "{power_pin}" and {power_en_pin} are configured now, waiting for "{power_pin}" fall.')
        GPIO.add_event_detect(power_pin, GPIO.FALLING, callback=self)

    def __call__(self, power_pin: int):
        self._log.info(f'Power pin "{power_pin}" dropped, initiate safe shutdown now.')
        shutdown()
