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

"""
This is the top-level library module for the SGP password generator.
SGP is an algorithm (originally published by Chris Zarate under the name
SuperGenPass) for hashing a password with a domain, to create a unique
password for each site.

Note: This Python version is designed to be portable to other languages (to
serve as a reference implementation).

It's probably a better reference implementation than the original, because
it's commented and a few things are neater or more explicit.

SuperGenPass Password Hashing Algorithm Copyright (C) Chris Zarate
Python port and comments by Matt Giuca and Tim Cuthbertson
Based on JavaScript version from
http://supergenpass.com/mobile/
(Should generate the exact same strings as the original JavaScript version)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License version 2,
as published by the Free Software Foundation.
"""

import re

# NOTE: This is SGP's md5 module, not the built-in Python library.
import md5

__all__ = ['sgp']

def sgp(passwd, domain, length=None):
    """
    Given a master password and domain, generates a custom password just for that
    site. The original password cannot be obtained from the generated
    password.

    passwd: str. The "master password".
    domain: str. The domain name of the site to generate a hash for.
        Use domain.url_to_domain to retrieve a domain from a URL.
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
        pass_cand = md5.b64_md5(pass_cand)

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
        pass_cand = md5.b64_md5(pass_cand)

    return pass_cand[:length]
