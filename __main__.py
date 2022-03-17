import argparse
import logging
from logging import StreamHandler
from logging.handlers import SysLogHandler
from sys import stdout

from config_file import ConfigFile
from copy_config_files import CopyConfigFiles
from install_as_service import write_init_d_script
from safe_shutdown import SafeShutdown
from switch_display import SwitchDisplay
from util import swap_config

hdmi = ConfigFile('/boot/config_hdmi.txt')
lcd = ConfigFile('/boot/config_lcd.txt')
current = ConfigFile('/boot/config.txt')

logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)-8s %(name)-12s %(message)s',
                    handlers=[
                        SysLogHandler(address='/dev/log'),
                        StreamHandler(stdout),
                    ])


# TODO add audio fix https://github.com/RetroFlag/GPiCase2-Script/blob/main/recalbox_install_gpi2.sh#L10


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--setup', help='Installs this script as self starting service.', action='store_true')
    parser.add_argument('--set_lcd', help='Swaps the config to use the LCD display, may be used with --reboot.',
                        action='store_true')
    parser.add_argument('--set_hdmi', help='Swaps the config to use the HDMI out, may be used with --reboot.',
                        action='store_true')
    parser.add_argument('--reboot', help='Reboots after config switch.', action='store_true')
    parser.add_argument('--wait_for_changes', help='Starts in listening mode and wait for power od display events.',
                        action='store_true')
    parser.add_argument('--create_config_files',
                        help='Creates new display config files.',
                        action='store_true')
    args = parser.parse_args()

    if args.setup:
        write_init_d_script()
        return

    if args.set_lcd:
        swap_config(lcd, current, args.reboot)
        return

    if args.set_hdmi:
        swap_config(hdmi, current, args.reboot)
        return

    if args.create_config_files:
        copy = CopyConfigFiles(config_hdmi=hdmi, config_lcd=lcd, config_current=current)
        copy.ensure_config_files_exists()
        return

    if args.wait_for_changes:
        copy = CopyConfigFiles(config_hdmi=hdmi, config_lcd=lcd, config_current=current)
        copy.ensure_config_files_exists()

        shutdown = SafeShutdown()
        switch_display = SwitchDisplay(config_hdmi=hdmi, config_lcd=lcd, config_current=current, reboot=args.reboot)

        switch_display.start()

        return

    parser.print_help()


if __name__ == "__main__":
    main()
