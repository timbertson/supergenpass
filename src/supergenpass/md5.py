# SGP Password Generator
# Portions Copyright (C) Chris Zarate
# Portions Copyright (C) 2008-2009 Matt Giuca, Tim Cuthbertson

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2,
# as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Author: Matt Giuca

"""
This module defines a custom MD5 hashing function, which hashes a string to a
Base-64-encoded MD5 hash string.

This code could be omitted in favour of the built-in md5 library, but it was
included for the following reasons:
- This code is a direct port of the original JavaScript version of
  SuperGenPass's MD5 algorithm. This ensures there is no discrepancy between
  the two implementations.
- It is designed to serve as a reference implementation of SuperGenPass (for
  porting to other languages), so it should contain its own implementation of
  MD5.
- This implementation is compatible with the original SuperGenPass's treatment
  of non-ASCII characters in Unicode strings (non-standard treatment).
- This implementation of Base-64 encoding pads with 'A' (compatible with the
  original SuperGenPass), while Python's pads with '='.
"""

__all__ = ['b64_md5']

def b64_md5(p):
    """
    Returns a Base64-encoded string which is the MD5 hash of the original
    string p.
    Note: If str is a Unicode string, it is treated quite awkwardly: the lower
    8 bits of each characters code point are used as a byte, and the rest is
    thrown away. This doesn't correspond to any Unicode encoding scheme.
    Be careful.
    (This is compatible with the main SuperGenPass implementation).

    Examples:
    >>> b64_md5('hello')
    'XUFAKrxLKna5cZ2REBfFkgAA'

    Note the non-standard treatment of non-ASCII characters:
    >>> b64_md5(u'm\u00fctable')
    'AtBqdjQCqTGwC1sfG40nVQAA'
    >>> b64_md5(u'o\u0123g')
    'lmlQrXG029Dwb7KlQ6COegAA'
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

def _test():
    import doctest
    doctest.testmod()
    
if __name__ == "__main__":
    _test()
