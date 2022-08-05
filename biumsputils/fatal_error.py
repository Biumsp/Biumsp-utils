from sys import exit
from biumsputils.print import print

def fatal_error(message):
	print('Error:' + message)
	sys.exit(1)
