#!/usr/bin/env python

# SuperGenPass Password Hashing Algorithm
# Copyright (C) Chris Zarate
# Python port and comments by Matt Giuca
# Based on JavaScript version from
# http://supergenpass.com/mobile/
# (Should generate the exact same strings as the original JavaScript version)

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2,
# as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.	If not, see <http://www.gnu.org/licenses/>.

# Usage:
# Either use as a library (import supergenpass), by calling the sgp function,
# or use as a command-line app.
# See supergenpass.py --help.

# Note: This Python version is designed to be portable to other languages (to
# serve as a reference implementation).
# I have deliberately avoided using Python libraries (except re), so the code
# may easily port to other languages which don't have those libraries.
# (For example, the MD5 code could have been replaced by a call to md5.md5,
# but then it wouldn't be portable to languages without an MD5 library).

# It's probably a better reference implementation than the original, because
# it's commented and a few things are neater or more explicit.

import re

def b64_md5(p):
	"""
	Returns a Base64-encoded string which is the MD5 hash of the original
	string p.
	Note: If str is a Unicode string, it is treated quite awkwardly: the lower
	8 bits of each characters code point are used as a byte, and the rest is
	thrown away. This doesn't correspond to any Unicode encoding scheme.
	Be careful.
	(This is compatible with the main SuperGenPass implementation).
	"""
	return binl2b64(core_md5(str2binl(p), len(p)*8))

def binl2b64(binarray):
	"""
	Given an array of 32-bit ints, converts into a Base64-encoded string.
	"""
	tab = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz012345678998'
	str = ''
	i = 0

	# Pad binarray with 0s (the JavaScript version didn't do this)
	# Will always access exactly 1 element past the end, so insert a 0
	binarray = extend_array_to_length(binarray, len(binarray)+1, 0)

	for i in range(0, (len(binarray)-1) * 4, 3):
		triplet = ((((binarray[i>>2]>>8*(i%4))&0xFF)<<16)
					| (((binarray[i+1>>2]>>8*((i+1)%4))&0xFF)<<8)
					| ((binarray[i+2>>2]>>8*((i+2)%4))&0xFF)
				  )
		for j in range(0, 4):
			str += tab[(triplet>>6*(3-j))&0x3F]
	return str

def extend_array_to_length(array, length, default=None):
	"""
	Concatenate instances of default to the end of an array, to ensure its
	length is at least "length".
	Returns the new array; does not modify the original. Always makes a copy
	and converts into a list, even if not modifying the array.
	Does not modify existing elements of the array.
	Does not modify the array at all if it is already long enough.
	"""
	if len(array) >= length:
		return list(array)
	return list(array) + [default] * (length - len(array))

def core_md5(x, length):
	"""
	Performs an MD5 hash on an array (x) of 32-bit unsigned ints, which
	represent octets stored in little-endian words.
	length: The number of bits to consider (noting that len(x)*32 may be
		longer than length, in which case the words are padded with 0s).
	"""
	# Allocate space for x (the JavaScript version didn't do this)
	max_access_x = max(length>>5 + 1, (((length+64)>>9)<<4) + 15)
	x = extend_array_to_length(x, max_access_x+1, 0)

	# Append a '1' bit to the end of the message
	x[length>>5] |= swrap(0x80 << ((length)%32))
	# Note: The following line originally used JavaScript's >>> operator
	# (unsigned right shift). I believe in Python we can use >> (signed right
	# shift) because the value would only have gone negative if it overflowed
	# (which doesn't happen in Python).
	x[(((length+64)>>9)<<4)+14] = length
	a = 1732584193
	b = -271733879
	c = -1732584194
	d = 271733878

	for i in range(0, len(x), 16):
		olda = a
		oldb = b
		oldc = c
		oldd = d
		a=md5_ff(a,b,c,d,x[i+0],7,-680876936); d=md5_ff(d,a,b,c,x[i+1],12,-389564586); c=md5_ff(c,d,a,b,x[i+2],17,606105819); b=md5_ff(b,c,d,a,x[i+3],22,-1044525330);
		a=md5_ff(a,b,c,d,x[i+4],7,-176418897); d=md5_ff(d,a,b,c,x[i+5],12,1200080426); c=md5_ff(c,d,a,b,x[i+6],17,-1473231341); b=md5_ff(b,c,d,a,x[i+7],22,-45705983);
		a=md5_ff(a,b,c,d,x[i+8],7,1770035416); d=md5_ff(d,a,b,c,x[i+9],12,-1958414417); c=md5_ff(c,d,a,b,x[i+10],17,-42063); b=md5_ff(b,c,d,a,x[i+11],22,-1990404162);
		a=md5_ff(a,b,c,d,x[i+12],7,1804603682); d=md5_ff(d,a,b,c,x[i+13],12,-40341101); c=md5_ff(c,d,a,b,x[i+14],17,-1502002290); b=md5_ff(b,c,d,a,x[i+15],22,1236535329);
		a=md5_gg(a,b,c,d,x[i+1],5,-165796510); d=md5_gg(d,a,b,c,x[i+6],9,-1069501632); c=md5_gg(c,d,a,b,x[i+11],14,643717713); b=md5_gg(b,c,d,a,x[i+0],20,-373897302);
		a=md5_gg(a,b,c,d,x[i+5],5,-701558691); d=md5_gg(d,a,b,c,x[i+10],9,38016083); c=md5_gg(c,d,a,b,x[i+15],14,-660478335); b=md5_gg(b,c,d,a,x[i+4],20,-405537848);
		a=md5_gg(a,b,c,d,x[i+9],5,568446438); d=md5_gg(d,a,b,c,x[i+14],9,-1019803690); c=md5_gg(c,d,a,b,x[i+3],14,-187363961); b=md5_gg(b,c,d,a,x[i+8],20,1163531501);
		a=md5_gg(a,b,c,d,x[i+13],5,-1444681467); d=md5_gg(d,a,b,c,x[i+2],9,-51403784); c=md5_gg(c,d,a,b,x[i+7],14,1735328473); b=md5_gg(b,c,d,a,x[i+12],20,-1926607734);
		a=md5_hh(a,b,c,d,x[i+5],4,-378558); d=md5_hh(d,a,b,c,x[i+8],11,-2022574463); c=md5_hh(c,d,a,b,x[i+11],16,1839030562); b=md5_hh(b,c,d,a,x[i+14],23,-35309556);
		a=md5_hh(a,b,c,d,x[i+1],4,-1530992060); d=md5_hh(d,a,b,c,x[i+4],11,1272893353); c=md5_hh(c,d,a,b,x[i+7],16,-155497632); b=md5_hh(b,c,d,a,x[i+10],23,-1094730640);
		a=md5_hh(a,b,c,d,x[i+13],4,681279174); d=md5_hh(d,a,b,c,x[i+0],11,-358537222); c=md5_hh(c,d,a,b,x[i+3],16,-722521979); b=md5_hh(b,c,d,a,x[i+6],23,76029189);
		a=md5_hh(a,b,c,d,x[i+9],4,-640364487); d=md5_hh(d,a,b,c,x[i+12],11,-421815835); c=md5_hh(c,d,a,b,x[i+15],16,530742520); b=md5_hh(b,c,d,a,x[i+2],23,-995338651);
		a=md5_ii(a,b,c,d,x[i+0],6,-198630844); d=md5_ii(d,a,b,c,x[i+7],10,1126891415); c=md5_ii(c,d,a,b,x[i+14],15,-1416354905); b=md5_ii(b,c,d,a,x[i+5],21,-57434055);
		a=md5_ii(a,b,c,d,x[i+12],6,1700485571); d=md5_ii(d,a,b,c,x[i+3],10,-1894986606); c=md5_ii(c,d,a,b,x[i+10],15,-1051523); b=md5_ii(b,c,d,a,x[i+1],21,-2054922799);
		a=md5_ii(a,b,c,d,x[i+8],6,1873313359); d=md5_ii(d,a,b,c,x[i+15],10,-30611744); c=md5_ii(c,d,a,b,x[i+6],15,-1560198380); b=md5_ii(b,c,d,a,x[i+13],21,1309151649);
		a=md5_ii(a,b,c,d,x[i+4],6,-145523070); d=md5_ii(d,a,b,c,x[i+11],10,-1120210379); c=md5_ii(c,d,a,b,x[i+2],15,718787259); b=md5_ii(b,c,d,a,x[i+9],21,-343485551);
		a=safe_add(a,olda); b=safe_add(b,oldb); c=safe_add(c,oldc); d=safe_add(d,oldd);

	return (a,b,c,d)

def ushr(num, bits):
	"""
	Unsigned right-shift (JavaScript's >>> operator)
	"""
	if num < 0:
		num += 0x100000000
	return int(num >> bits)
def md5_cmn(q, a, b, x, s, t):
	return safe_add(bit_rol(safe_add(safe_add(a, q), safe_add(x, t)), s), b)
def md5_ff(a, b, c, d, x, s, t):
	return md5_cmn((b&c) | ((~b) & d), a, b, x, s, t)
def md5_gg(a,b,c,d,x,s,t):
	return md5_cmn((b&d) | (c & (~d)), a, b, x, s, t)
def md5_hh(a,b,c,d,x,s,t):
	return md5_cmn(b^c^d, a, b, x, s, t)
def md5_ii(a,b,c,d,x,s,t):
	return md5_cmn(c ^ (b | (~d)), a, b, x, s, t)
def safe_add(x,y):
	lsw = (x & 0xFFFF) + (y & 0xFFFF)
	msw = (x >> 16) + (y >> 16) + (lsw >> 16)
	return swrap(msw << 16) | (lsw & 0xFFFF)
def bit_rol(num,cnt):
	return swrap(num << cnt) | ushr(num, 32-cnt)
def swrap(num):
	"""
	Signed 32-bit integer wrap.
	Takes a number and mods it into signed 32-bit integer space.
	Used whenever << might overflow. In JavaScript, << wraps in signed 32-bit
	space. In Python, it just keeps multiplying. This function keeps it in
	that space.
	(This is not necessary in a language with fixed-size signed integers).
	"""
	num = num & 0xFFFFFFFF
	if num > 0x7FFFFFFF:
		return int(num - 0x100000000)
	else:
		return int(num)

def str2binl(str):
	"""
	Convert a string into a list of 32-bit unsigned ints in little-endian.

	Note: If str is a Unicode string, it is treated quite awkwardly: the lower
	8 bits of each characters code point are used as a byte, and the rest is
	thrown away. This doesn't correspond to any Unicode encoding scheme.
	Be careful.
	(This is compatible with the main SuperGenPass implementation).
	"""
	# Allocate space (all zeroes) in advance
	bin = [0] * ((len(str) + 3) // 4)
	for i in range(0, len(str)):
		# XXX If str is a unicode string, this will truncate the higher bytes
		# of the code point for non-ASCII characters. This behaviour is
		# retained as it is compatible with the main implementation.
		# If translating this code to a language which doesn't support Unicode
		# strings, be aware that you may get different results if, for
		# example, strings are stored as UTF-8.
		bin[i//4] |= (ord(str[i]) & 0xFF) << ((i*8) % 32)
	return bin

def sgp(passwd, domain, length=None):
	"""
	Given a master password and domain, generates a custom password just for that
	site. The original password cannot be obtained from the generated
	password.

	passwd: str. The "master password".
	domain: str. The domain name of the site to generate a hash for.
	length: int. Length of the generated password hash. Must be between 4 and
		24 inclusive. Defaults to 10.
	"""
	if length is None:
		length = 10
	# Typecheck and validate
	if not isinstance(passwd, basestring):
		raise TypeError("sgp: passwd must be a string")
	if not isinstance(domain, basestring):
		raise TypeError("sgp: domain must be a string")
	if not isinstance(length, int) and not isinstance(length, long):
		raise TypeError("sgp: length must be an int")
	if len(passwd) == 0:
		raise ValueError("sgp: passwd must not be empty")
	if len(domain) == 0:
		raise ValueError("sgp: domain must not be empty")
	if not 4 <= length <= 24:
		raise ValueError("sgp: length must be between 4 and 24 inclusive")

	# Salt the password with the domain
	pass_cand = passwd + ':' + domain
	# MD5-hash it ten times
	for i in range(10):
		pass_cand = b64_md5(pass_cand)

	# It must start with a lowercase letter and contain at least one uppercase
	# letter and one number (to comply with password requirements).
	# Keep hashing it until it meets these conditions.
	def valid_password(pass_cand):
		"""
		Return True if the password meets these criteria; False otherwise.
		"""
		t = re.search("[a-z]", pass_cand)
		if t is None:
			return False
		if t.start() != 0:
			return False
		return bool(re.search("[A-Z]", pass_cand)
				and re.search("[0-9]", pass_cand))

	while not valid_password(pass_cand[:length]):
		pass_cand = b64_md5(pass_cand)

	return pass_cand[:length]

### COMMAND-LINE SPECIFIC CODE ###

import sys
import getopt
import getpass

from domain import domain_for_url
def usage(progname):
	print "SuperGenPass"
	print "Prompts for a master password and domain name."
	print "Generates a custom password for that domain."
	print
	print "Usage: %s [OPTIONS] [URL]" % progname
	print "	   URL			The URL/domain name to make a password for"
	print "					(Will prompt if not supplied)"
	print "	   OPTIONS"
	print "		   -l		Generated password length"
	print "		   --help	This help"

def main(argv=None):
	if argv is None:
		argv = sys.argv
	if len(argv) == 0:
		argv = ["supergenpass.py"]

	try:
		opts, args = getopt.getopt(argv[1:], "l:", ["help"])
	except getopt.error, msg:
		 usage(argv[0])
		 return 1

	# process options
	length = None
	for o, a in opts:
		if o == "--help":
			usage(argv[0])
			return 1
		elif o == "-l":
			try:
				length = int(a)
			except ValueError:
				print "length must be an int"
				print "for help, type %s --help" % argv[0]
				return 1

	if length is not None and not 4 <= length <= 24:
		print "length must be between 4 and 24 inclusive"
		return 1

	try:
		passwd = getpass.getpass("Enter master password: ")
	except (EOFError, KeyboardInterrupt):
		print
		return 2
	if len(passwd) == 0:
		return 2

	if len(args) == 0:
		# Prompt for the domain
		try:
			url = raw_input("Enter URL/domain: ")
		except (EOFError, KeyboardInterrupt):
			print
			return 2
	else:
		url = args[0]
	if len(url) == 0:
		return 2

	# Point of contention: We decode these as UTF-8, so as to mirror the
	# behaviour on the site (which is to treat non-ASCII characters
	# specially). See discussion above.
	try:
		passwd = passwd.decode("utf-8")
		url = url.decode("utf-8")
	except UnicodeDecodeError:
		print "Input was not in UTF-8"
		return 1

	domain = domain_for_url(url)
	password = sgp(passwd, domain, length)
	print "Domain: '%s'" % domain
	print "password: %s" % password

if __name__ == "__main__":
	sys.exit(main())
