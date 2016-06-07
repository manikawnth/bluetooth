# file: rfcomm-client.py
# auth: Albert Huang <albert@csail.mit.edu>
# desc: simple demonstration of a client application that uses RFCOMM sockets
#       intended for use with rfcomm-server
#
# $Id: rfcomm-client.py 424 2006-08-24 03:35:54Z albert $

from bluetooth import *
import subprocess
import obd
import time


host = '00:1D:A5:00:0F:B6'
port = 1

#retcode = subprocess.call("rfcomm connect /dev/rfcomm0 00:1D:A5:00:0F:B6 1 &",shell=True)
#print("Return code is:", retcode)

proc = subprocess.Popen(["rfcomm", "connect", "/dev/rfcomm0", "00:1D:A5:00:0F:B6", "1","&"])
time.sleep(10)
print("Slept for 10 secs: Command should have completed")
conn = obd.OBD("/dev/rfcomm0")
cmd = obd.commands.DISTANCE_SINCE_DTC_CLEAR
print("querying OBD")
resp = conn.query(cmd)
print(resp.value,resp.unit)
proc2 = subprocess.Popen(["rfcomm", "release", "/dev/rfcomm0"])
time.sleep(5)
print("Disconnected")
