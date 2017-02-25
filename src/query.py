import sys

def server():
	sys.stdout.write("$> ")
	sys.stdout.flush()

def client():
	sys.stdout.write("[You]: ")
	sys.stdout.flush()

# process commands - TODO
def command(cmd):
	if "/exit" in cmd:
		exit()
