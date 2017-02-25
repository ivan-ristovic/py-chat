# TCP Chat Client implementation

import select, socket, string, sys
import query

# main
if __name__ == "__main__":

	if len(sys.argv) < 3:
		print "usage: %s <hostname> <port>" % sys.argv[0]
		sys.exit()

	host = sys.argv[1]
	port = int(sys.argv[2])

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(2)

	# connecting to host
	try:
		s.connect((host, port))
	except:
		print ">> Connection failed."
		sys.exit()

	print ">> Connected to remote host"
	query.client()

	while True:
		# we are listening from stdin (user message) and server socket
		socket_list = [sys.stdin, s]

		# fetching readable socket list
		read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])

		for sock in read_sockets:
			# checking if there is an incomming message from server
			if sock == s:
				data = sock.recv(4096)
				if not data:
					print ">> Connection timed out."
					sys.exit()
				else:
					#print data
					sys.stdout.write(data)
			else: # otherwise user entered a message
				msg = sys.stdin.readline()
				if "/exit" in msg:
					exit()
				s.send(msg)

			query.client()
