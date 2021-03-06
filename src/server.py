# TCP Chat Server implementation

import select, socket, sys
import query

# broadcasts message to all clients connected to server
def broadcast(sender_socket, message):
	for socket in CONNECTION_LIST:
		# no sense to send message to server or client that sent the message
		if socket != server_socket and socket != sender_socket:
			try:
				socket.send(message)
			except:
				# client closed the socket, so we remove it
				socket.close()
				CONNECTION_LIST.remove(socket)

# main
if __name__ == "__main__":

	if len(sys.argv) != 2:
		exit("usage: %s <port>" % sys.argv[0])

	# connection list
	CONNECTION_LIST = []
	# receive buffer length
	RECV_BUFFER = 4096
	# listen port
	try:
		PORT = int(sys.argv[1])
		if PORT < 1000 or PORT > 60000:
			raise ValueError
	except ValueError:
		exit(">> Invalid port.")

	# creating and configuring server socket
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server_socket.bind(("0.0.0.0", PORT))
	server_socket.listen(10)

	# adding socket to list
	CONNECTION_LIST.append(server_socket)

	CONNECTION_LIST.append(sys.stdin)

	print "\r>> Server started on port:", PORT

	query.server()

	while True:
		# fetching connection list
		read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])

		for sock in read_sockets:
			# if the new connection is received through server socket
			if sock == sys.stdin:
				cmd = sys.stdin.readline()
				query.command(cmd)
			elif sock == server_socket:
				sockfd, addr = server_socket.accept()
				CONNECTION_LIST.append(sockfd)
				print "\r>> (%s, %s) connected." % addr
				broadcast(sockfd, "\r>> [%s:%s] entered chat room.\n" % addr)
			else:	# otherwise we received message from client
				try:
					data = sock.recv(RECV_BUFFER)
					if data == "":
						raise Exception
					if data:
						broadcast(sock, "\r" + str(sock.getpeername()) + ": " + data)
						print "\r" + str(sock.getpeername()) + ": " + data,
				except:
					broadcast(sock, "\r>> [%s, %s] is now offline.\n" % addr)
					print "\r>> (%s, %s) is now offline." % addr
					if sock in CONNECTION_LIST:
						sock.close()
						CONNECTION_LIST.remove(sock)
					continue

			query.server()

	server_socket.close()
