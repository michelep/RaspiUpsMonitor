import time
import sys
import os

from config import Config
from max17034 import Max17034

class UPSMonitor:
    def __init__(self):
	Config.log.info("Raspi UPS Monitor is starting...")
	self.max17034 = Max17034(0x34,Config.i2c_bus)
	self.status = 0
	self.last_cap = 0

    def do_action(self, action):
	args = action.split()
	try:
	    os.execv(args[1],args[2:])
	except OSError as err:
	    Config.log.error("ERROR while executing %s:%s"%(action,err))

    def run(self):
	while(True):
#    	    v = self.max17034.readVoltage()
	    c = self.max17034.readCapacity()

	    if c > self.last_cap:
		self.last_cap = c
		self.status = 1 # Charging..
	    else:
		self.last_cap = c
		self.status = 0 # Discharging....

		if(c < Config.alert_level):
		    if(c < Config.critical_level):
			# CRITICAL !!!
			Config.log.warning("UPS Battery has reached a critical level (%d%%)",c)
			self.do_action(Config.critical_action)
		    else:
			# ALERT !!!
			Config.log.warning("UPS Battery has reached alert level (%d%%)",c)
			self.do_action(Config.alert_action)

	    Config.log.debug("%(volt).2fV (%(cap)i%%) status: %(status)" % { 'volt': v, 'cap': c, 'status': self.status } )
	    time.sleep(60)
