import sys

def server():
	sys.stdout.write("$> ")
	sys.stdout.flush()

def client():
	sys.stdout.write("[You]: ")
	sys.stdout.flush()
