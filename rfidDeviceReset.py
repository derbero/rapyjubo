import usb.core
import usb.util
import sys
from time import gmtime, strftime
import time

print ("Now: ",strftime("%Y-%m-%d %H:%M:%S", gmtime()))


# find our device
dev = usb.core.find(idVendor=0xffff, idProduct=0x0035)

# was it found?
if dev is None:
    raise ValueError('Device not found')
else:
    print ("Device found! Resetting")
    dev.reset()
    
