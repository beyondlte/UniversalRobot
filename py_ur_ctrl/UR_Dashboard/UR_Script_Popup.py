import socket
import time
"""
HOST = "172.31.1.147"     # The remote host
PORT = 30001              # The same port as used by the server
print "Starting Program"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT))
#s.send('popup("Popup Test Message", title="Title", blocking=True)' + '\n') 
s.send('get_actual_tcp_pose()' +'\n')
data = s.recv(1024)
s.close()
print("Recived", (data))
"""
HOST = "172.31.1.147"     # The remote host
PORT = 29999 # The same port as used by the server
print "Starting Program"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT))
# s.send('popup("Popup Test Message", title="Title", blocking=True)' + '\n') 
# s.send('running' +'\n')
s.send('get loaded program' +'\n')
data = s.recv(4096)
data1= s.recv(1024)
# only the first connection will send two messages back from UR
# 1. Connected: Universal Robots Dashboard Server
# 2. ...
print("Received", (data))
print("Received", (data1))

# load the program a3.urp
if "No program loaded" in data1:
	s.send('load /programs/a3/a3.urp' + '\n')
	data1= s.recv(1024)
	print("Received", (data1))

# first release brake 
time.sleep(0.5)
s.send('brake release' + '\n')
data = s.recv(4096)
print("Received", (data))

time.sleep(1.0)
s.send('play' + '\n')
data = s.recv(4096)
print("Received", (data))
startTime = time.clock()
elapsedTime = 0.0

runningCheck = False
# it takes about 13s to start the program
while elapsedTime < 15.0 and  runningCheck == False:
	s.send('running' + '\n')
	runningStatus = s.recv(4096)
	print runningStatus
	runningCheck = ('Program running: true' in runningStatus)
	time.sleep(1.0)
	elapsedTime = time.clock() - startTime

s.close()
