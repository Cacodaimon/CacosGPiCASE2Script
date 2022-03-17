import logging
import os
from os import system
from os.path import dirname
from shutil import copyfile

from util import copy_resource_to_file

log = logging.getLogger(__name__)


def write_init_d_script():
    file_name = '/etc/init.d/S99CacosGPiCase2Script'
    system('mount -o remount, rw /')
    copy_resource_to_file('init.d/S99CacosGPiCase2Script', file_name)
    _make_executable(file_name)
    copyfile(dirname(__file__), '/opt/cacos_gpicase2_script.zip')
    log.info(f'Installed /opt/cacos_gpicase2_script.zip as service.')


def _make_executable(path):
    # from https://stackoverflow.com/a/30463972
    mode = os.stat(path).st_mode
    mode |= (mode & 0o444) >> 2  # copy R bits to X
    os.chmod(path, mode)
