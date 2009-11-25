#!/usr/bin/env python

from telnetlib import Telnet
import sys

CONTINUE = 'repl> '
class NoResponse(RuntimeError): pass

def _get(tel):
	response = tel.read_until(CONTINUE, 2)
	if not response:
		raise NoResponse()
	lines = response.splitlines()
	if lines[-1] == CONTINUE:
		lines = lines[:-1]
	return lines

def main():
	print get()

def get(host='localhost', port=4242):
	tel = Telnet(host, port)
	_get(tel)
	tel.write('content.location.href')
	result = _get(tel)
	tel.close()
	return result[0].strip('"')

if __name__ == '__main__':
	sys.exit(main())
