# CacosGPiCASE2Script

A replacement for the official [GPiCase2-Script](https://github.com/RetroFlag/GPiCase2-Script), for use with [Recalbox 8.0.x](https://www.recalbox.com/) only. Please do not forget to install the [Display Patch]()

I had too much trouble with the original script. Therefore, I wrote this more robust and simpler to use/install replacement. It still performs a full reboot after connecting to or disconnecting from the docking station.

Tested with Recalbox 8.0.2 and a Raspberry PI CM4104032 (4GB RAM, 32GB Flash, WLAN + BT).

## Installation instructions

1. Connect your GPiCase2 to your Wi-Fi
2. Login via SSH (The default password is **recalboxroot**)

```sh
ssh root@recalbox
```

3. Download the script as ZIP container via wget: 

```sh
wget -O /tmp/CacosGPiCASE2_Script.zip https://github.com/Cacodaimon/CacosGPiCASE2Script/blob/main/CacosGPiCASE2_Script.zip?raw=true
```

4. Install the script using the self installation function

```sh
python /tmp/CacosGPiCASE2_Script.zip --setup
```

5. Reboot your GPiCase2

```sh
shutdown -r now
```

## Other useful commands

### Install display config files

This script comes with the both [modified](https://github.com/Cacodaimon/CacosGPiCASE2Script/blob/main/configs/config_hdmi.txt#L35) Display Patch files (`config_lcd.txt` and `config_hdmi.txt`) from RetroFlag, you can install them using the following command:

```sh
python /tmp/CacosGPiCASE2_Script.zip --create_config_files
```

Use the `--force` option for overwriting exiting files.

```sh
python /tmp/CacosGPiCASE2_Script.zip --create_config_files --force
```

### Testing without installation

Once downloaded via `wget` you can test the script without installation, you might download it again after reboot.
For a dry run omit the `--reboot` flag.

```sh
python /tmp/CacosGPiCASE2_Script.zip --wait_for_changes --reboot
```

### Force HDMI or LCD


```sh
python /tmp/CacosGPiCASE2_Script.zip --set_lcd|--set_hdmi
```

### Logging

You should find all infos in the recalbox's syslog.

```sh
tail -f /var/log/messages
```

```
Jan  1 02:00:15 RECALBOX user.info INFO     copy_config_files Check all config files already exist.
Jan  1 02:00:15 RECALBOX user.info INFO     safe_shutdown Configuring GPIO pin "26" and "27".
Jan  1 02:00:15 RECALBOX user.info INFO     safe_shutdown GPIO pin "26" and 27 are configured now, waiting for "26" fall.
Jan  1 02:00:16 RECALBOX user.info INFO     switch_display Currently connected to LCD, pin "18" is LOW.
Jan  1 02:00:16 RECALBOX user.info INFO     switch_display Waiting for HDMI connect now.
```

## Uninstall

1. Login via SSH (The default passwort is **recalboxroot**)

```sh
ssh root@recalbox
```

2. Delete the both files:

```sh
rm /etc/init.d/S99CacosGPiCase2Script
rm /opt/cacos_gpicase2_script.zip
```

3. Reboot your GPiCase2

```sh
shutdown -r now
```

## Known issues

Here are some other issues I ran into during my GPiCase2 installation nightmare.

### The LCD is blank

You must hear **two** clicking sounds, one for each connector row, when placing the CM4 in the GPiCase2.
My CM4 booted, was reachable via WiFi, even the HDMI out worked, but the LCD kept blank until I mounted the CM4 correctly.   

### How can I flash a CM4 with eMMC memory?

You can use the build in micro USB port (above the GPiCase2's CM4 slot) to mount the eMMC memory as a storage!

Follow these instructions [How to flash Raspberry Pi OS onto the Compute Module 4 eMMC with usbboot](https://www.jeffgeerling.com/blog/2020/how-flash-raspberry-pi-os-compute-module-4-emmc-usbboot), an **IO Board** is not needed, go directly to section "Using usbboot to mount the eMMC storage". You will find a recent version of Recalbox when using the **Raspberry Pi Imager** in the **Emulation and game OS section**!

You won't be able to use the **microSD** slot, but do not blame RetroFlag this time. [A CM4 with eMMC can not use the microSD card](https://forums.raspberrypi.com/viewtopic.php?t=305506).

### I hear no sound when connected to HDMI

Please go to the settings menu and check if sound output device is HDMI:

![Main menu](https://raw.githubusercontent.com/Cacodaimon/CacosGPiCASE2Script/main/media/%20HDMI%20Sound%2001.png)
![Sound settings](https://raw.githubusercontent.com/Cacodaimon/CacosGPiCASE2Script/main/media/%20HDMI%20Sound%2002.png)
![Output device](https://raw.githubusercontent.com/Cacodaimon/CacosGPiCASE2Script/main/media/%20HDMI%20Sound%2003.png)

### HDMI settings

If you have issues with your HDMI display, you might need to fiddle around with your PI's HDMI settings like `hdmi_group`, `hdmi_mode`, `disable_overscan` etc..
Add the settings to the [`recalbox-user-config.txt`](https://wiki.recalbox.com/en/tutorials/video/display-configuration/image-size-settings-overscan-tft) according the Recalbox WIKI.