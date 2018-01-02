# RaspiUpsMonitor
a Python monitor script for Raspi UPS HAT

Raspi UPS HAT was an HAT for Raspberry Pi with a battery, that act like an UPS. On board, there's a MAX17034 chip (connected to i2c bus) that reply with voltage and remaining capacity.
With this simple script, far to be perfect (and you are encouraged to fix and improve it !), you can shutdown safely your RPi when battery on UPS Hat reach a critical level, avoid any potentials data loss.

