import logging
import pkgutil
from os import system
from sys import exit

from config_file import ConfigFile


def copy_resource_to_file(resource_name: str, file_name: str):
    log = logging.getLogger(__name__)
    log.info(f'Copy "{resource_name}" to "{file_name}".')
    data = pkgutil.get_data(__name__, resource_name)
    with open(file_name, 'wb') as f:
        f.write(data)
    log.info(f'Done writing "{file_name}".')


def shutdown(reboot: bool = False):
    log = logging.getLogger(__name__)
    log.info('Issuing immediate reboot.' if reboot else 'Issuing immediate shutdown.')
    halt_or_reboot = '-r' if reboot else '-h'
    system(f'shutdown {halt_or_reboot} now "GPi CASE2 Power switch turned off!"')
    exit()


def swap_config(new_config: ConfigFile, current_config: ConfigFile, reboot: bool = False):
    log = logging.getLogger(__name__)
    log.info(f'Swapping configuration with "{new_config.base_name}".')
    system('mount -o remount, rw /boot')
    system(f'cp {new_config.file_name} {current_config.file_name}')
    log.info(f'Swapped configuration with "{new_config.base_name}".')

    if reboot:
        log.info(f'Rebooting after config change with "{new_config.base_name}".')
        shutdown(reboot=True)
