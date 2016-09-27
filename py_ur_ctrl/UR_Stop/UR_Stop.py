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


# first release brake 
time.sleep(0.5)
s.send('stop' + '\n')
data = s.recv(4096)
print("Received", (data))

runningMode = "false"
while runningMode == "false":
    s.send('running' + '\n')
    runningStatus = s.recv(4096)
    runningMode = ("false" in runningStatus)
    time.sleep(1.0)

s.close()
