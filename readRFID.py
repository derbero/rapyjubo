from rfidhid.core import RfidHid

try:
    # Try to open RFID device using default vid:pid (ffff:0035)
    rfid = RfidHid()
except Exception as e:
    print(e)
    exit()

payload_response = rfid.read_tag()
uid = payload_response.get_tag_uid()

rfid.beep()
print(uid)
