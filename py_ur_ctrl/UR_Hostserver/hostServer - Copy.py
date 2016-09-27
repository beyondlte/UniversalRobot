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

while True:
	# Wait for a connection
	print >>sys.stderr, 'waiting for a connection'
	connection, client_address = sock.accept()
	print connection
	print client_address

	try:
		print >>sys.stderr, 'connection from', client_address

		# Receive the data in small chunks and retransmit it
		mycmd = ""
		while True:
			data = connection.recv(1024)
			print >>sys.stderr, 'received "%s"' % data
			if 'Connection established' in data and mycmd == "":
				msg = '[0]'
				print >>sys.stderr, 'Sending %s to the client: 1\n' % msg 
				# connection.sendall(data)
				connection.sendall(msg + '\\10')

			elif mycmd == "move to home": # 'SET cmd_code 0' in data: 
				msg = '[12]'
				print >>sys.stderr, 'Sending %s to the client: 1\n' % msg 
				connection.sendall(msg + '\\10')
				time.sleep(2.0)
				mycmd = ""
			# elif 'SET cmd_code 12' in data and 'SET cmd_status 2' in data:
			# 	connection.sendall('[0]'+ '\\10')
			# 	time.sleep(1.0)
			# 	msg = '[16,1]'
			# 	print >>sys.stderr, 'Sending %s to the client: 1\n' % msg 
			# 	time.sleep(2.0)
			# 	connection.sendall(msg + '\\10')
			else:
				print >>sys.stderr, 'Sending nothing to the client'
				mycmd = raw_input('please enter your command:')
				connection.sendall('[0]' + '\\10')
				
				# break
			time.sleep(2.0)
			
	finally:
		# Clean up the connection
		connection.close()

