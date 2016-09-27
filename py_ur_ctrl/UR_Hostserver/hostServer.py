import socket
import sys
import time

# this only works with the echoClient.py, not the socketClient.py
# if we need 5 recv in server, then in client, we also need to call recv 5 times

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('172.31.1.100', 50000)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)


# Listen for incoming connections
sock.listen(1)

ctrlCmd = ""
while True:

	if ctrlCmd == 'start server':
		# Wait for a connection
		print >>sys.stderr, 'waiting for a connection'
		connection, client_address = sock.accept()

	elif ctrlCmd == 'start program':
		os.system('..\UR_Dashboard\UR_Script_Popup.exe')

	elif ctrlCmd == 'move to home':
		while True:
			data = connection.recv(1024)
			print >>sys.stderr, 'received "%s"' % data
			if 'Connection established' in data and mycmd == "":
				msg = '[0]'
				print >>sys.stderr, 'Sending %s to the client: 1\n' % msg 
				# connection.sendall(data)
				connection.sendall(msg + '\\10')
			elif 'SET cmd_code 0' in data:
				msg = '[12]'
				print >>sys.stderr, 'Sending %s to the client: 1\n' % msg 
				connection.sendall(msg + '\\10')
				time.sleep(2.0)
			else:
				break
	elif ctrlCmd == 'quit':
		break
	else:
		ctrlCmd = raw_input('tell me what to do:')

connection.close()

