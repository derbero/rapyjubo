from rfidhid.core import RfidHid
import usb.core
import usb.util
import sys

def initRFID():
	try:
		# Try to open RFID device using default vid:pid (ffff:0035)
		rfid = RfidHid()
		return rfid
	except Exception as e:
		print(e)
		exit()
		

def readRFID(rfid):
	payload_response = rfid.read_tag()
	uid = payload_response.get_tag_uid()

	rfid.beep()
	print(uid)
	return uid
	

def resetUSBconnection()
    VENDOR_ID = 0xffff
    PRODUCT_ID = 0x0035
    DATA_SIZE = 1
    device = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)
    if device is None:
        sys.exit("Could not find Keyboard")

    if device.is_kernel_driver_active(0):
        try:
                device.detach_kernel_driver(0)
                print "kernel driver detached"
        except usb.core.USBError as e:
                sys.exit("Could not detach kernel driver: %s" % str(e))
    else:
        print "no kernel driver attached"
#    try:
#        usb.util.claim_interface(device, 0)
#        print "claimed device"
#    except:
#        sys.exit("Could not claim the device: %s" % str(e))
    try:
        device.set_configuration()
        device.reset()
    except usb.core.USBError as e:
        sys.exit("Could not set configuration: %s" % str(e))

######### main
resetUSBconnection()
rfid = initRFID()
while True:
	sleep(1)
	card = readRFID(rfid)
	print ("Card read: " + str(card))
