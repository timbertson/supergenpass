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
This module provides the functionality of converting a URI into a Domain, for
use with the SGP algorithm.

The SGP algorithm takes a "domain" as input. Although technically the "domain"
may be an arbitrary string, it is usually an Internet domain name.

Pulling the domain name out of a URI is usually desirable, due to the
multitude of URLs which might share the same login details.
"""

import os.path
import re

__all__ = ['url_to_domain', 'domainlist']

# Filename of the Common Second-Level Domains list file, relative to the
# script directory
DOMAINLIST_FILE = "domainlist.txt"

def read_domain_list():
    """
    Reads the domain list from the domain list file, and returns it as a
    sequence of strings.
    """
    filename = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            DOMAINLIST_FILE)
    file = open(filename)
    try:
        for line in file:
            yield line.strip()
    finally:
        file.close()

domainlist = list(read_domain_list())
domainset = set(domainlist)
domainisolator = re.compile("([^/:]+)")

def url_to_domain(url):
    """
    Strip out everything from the URI but part of the hostname.
    This is defined as follows:
        1. Get the hostname portion of the URI.
        2. Take the top-level and second-level domain from the hostname.
        3. If the second-level domain is one of the known common second-level
           domains, take the third-level domain as well.

    The "known common second-level domains" (CSLDs) is unspecified in the
    algorithm (it is a large set of hard-coded SLDs). Hence it is a good idea
    to keep an eye on the actual domain generated, to make sure it is not too
    general.

    Examples:
    >>> url_to_domain("google.com")
    'google.com'
    >>> url_to_domain("www.google.com")
    'google.com'
    >>> url_to_domain("http://www.google.com/search?q=supergenpass")
    'google.com'
    >>> url_to_domain("http://www.google.com.au/search?q=supergenpass")
    'google.com.au'
    """
    hostname = url.strip()
    hostname = hostname.replace("http://", "")
    hostname = hostname.replace("https://", "")
    hostname = domainisolator.match(hostname).groups()[0]
    hostname = hostname.split(".")

    # We will still want to throw away most of the hostname
    if len(hostname) >= 2:
        # Take the top-level and second-level domain
        domain = hostname[len(hostname) - 2] + '.' + hostname[len(hostname) - 1]
        # If this is one of the known second-level domains, take the third
        # level as well
        if domain in domainset and len(hostname) >= 3:
            domain = hostname[len(hostname) - 3] + '.' + domain
    else:
        domain = '.'.join(hostname)
    
    return domain

def _test():
    import doctest
    doctest.testmod()
    
if __name__ == "__main__":
    _test()
