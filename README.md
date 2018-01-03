RaspiUpsMonitor
===============

### a Python monitor script for Raspi UPS HAT

Raspi UPS HAT was an HAT for Raspberry Pi with a battery, that act like an UPS. On board, there's a MAX17034 chip (connected to i2c bus) that could be asked for battery voltage and remaining capacity (0-100%).
With this simple script, far to be perfect (and you are encouraged to fix and improve it !), you can shutdown safely your RPi when battery on UPS Hat reach a critical level, avoid any potentials data loss.

### Install

Installation is pretty simple: just do *python setup.py build* and *sudo python setup.py install*. Because script need to be run as root, sould be a great idea to launch it on boot using init.d 

### Configure

Configuration is in raspiupsmonitor.cfg and the relevant part is [Monitor]:

    [Monitor]
    # On alert level of 10%, just alert all users...
    alert_level=10
    alert_action=/usr/bin/wall "UPS Battery is dying..."
    # When battery is dying, halt the system safely
    critical_level=5
    critical_action=/sbin/halt -p

"level" is the percentage of power remained, in a range from 0 to 100. When battery is discharging and reach the alert or critical level, "action" was executed.
