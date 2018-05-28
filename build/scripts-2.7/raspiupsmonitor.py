#!/usr/bin/python
#
# Raspi UPS Monitor
#
# Michele <o-zone@zerozone.it> Pinassi
#
# Ispired by Geekworm UPS "voltage and capacity" script and some other resources available on the net
#
import os
import sys
import logging
import ConfigParser
import time
import signal

from RaspiUpsMonitor.config import Config
from RaspiUpsMonitor.max17034 import Max17034

def do_action(action):
    args = action.split()
    if len(args) > 1:
	argv = args[1:]
    else:
	argv = None

    try:
	os.execv(args[0],argv)
    except OSError as err:
	Config.log.error("ERROR while executing %s:%s"%(action,err))


Config.is_run = True

# Stop handler
def handler_stop_signals(signum, frame):
    Config.is_run = False

# MAIN()
if __name__ == '__main__':
    Config.config_file = ['/etc/raspiupsmonitor.cfg', os.path.expanduser('~/.raspiupsmonitor.cfg'), 'raspiupsmonitor.cfg']

    conf = ConfigParser.ConfigParser()
    conf.read(Config.config_file)
    
    Config.i2c_bus = int(conf.get('General','i2c_bus'))
    Config.log_file = conf.get('General','log_file')
    Config.pid_file = conf.get('General','pid_file')
    Config.alert_level = int(conf.get('Monitor','alert_level'))
    Config.alert_action = conf.get('Monitor','alert_action')
    Config.critical_level = int(conf.get('Monitor','critical_level'))
    Config.critical_action = conf.get('Monitor','critical_action')

    if os.geteuid() != 0:
	print "Need to be run as root. Exiting."
	sys.exit()

    if Config.log_file:
	logging.basicConfig(level=logging.DEBUG, format="%(asctime)s;%(levelname)s;%(message)s")
	flh = logging.FileHandler(Config.log_file, "w")
    else:
	flh = logging.NullHandler()

    Config.log = logging.getLogger(__name__)
    Config.log.addHandler(flh)

    if os.path.isfile(Config.pid_file):
	print "PID file exists"
	sys.exit()

    pid = str(os.getpid())
    file(Config.pid_file, 'w').write(pid)

    # Catch program termination
    signal.signal(signal.SIGINT, handler_stop_signals)
    signal.signal(signal.SIGTERM, handler_stop_signals) # CTRL+C
    signal.signal(signal.SIGTSTP, handler_stop_signals) # CTRL+Z

    Config.log.info("Raspi UPS Monitor is starting (i2c bus %d)..."%(Config.i2c_bus))
    max17034 = Max17034(0x36,Config.i2c_bus)
    status = 0
    last_cap = 0

    while(Config.is_run):
	v = max17034.readVoltage()
	c = max17034.readCapacity()

	Config.log.debug("%(volt).2fV (%(cap)i%%)" % { 'volt': v, 'cap': c } )

	if c > last_cap:
	    last_cap = c
	    status = 1 # Charging..
	elif c < last_cap:
	    last_cap = c
	    status = 0 # Discharging....

	    if(c < Config.alert_level):
		if(c < Config.critical_level):
		    # CRITICAL !!!
		    Config.log.warning("UPS Battery has reached a critical level (%d%% < %d%%)",c,Config.critical_level)
		    do_action(Config.critical_action)
		else:
		    # ALERT !!!
		    Config.log.warning("UPS Battery has reached alert level (%d%% < %d%%)",c,Config.alert_level)
		    do_action(Config.alert_action)
	else:
	    # No changes
	    pass

	Config.log.debug("Status: %d Last Cap: %d"%(status,last_cap))

	time.sleep(60)

    os.unlink(Config.pid_file)
    Config.log.info("Raspi UPS Monitor ended")
