#!/usr/bin/env python

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

# Usage: see sgp --help
# Also available as a library (import supergenpass).

import sys
import getopt
import getpass

import supergenpass
import supergenpass.domain

def usage(progname):
    print "SuperGenPass"
    print "Prompts for a master password and domain name."
    print "Generates a custom password for that domain."
    print
    print "Usage: %s [OPTIONS] [URL]" % progname
    print "    URL          The URL/domain name to make a password for"
    print "                 (Will prompt if not supplied)"
    print "    OPTIONS"
    print "        -l       Generated password length"
    print "        --help   This help"

def main(argv=None):
    if argv is None:
        argv = sys.argv

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

    domain = supergenpass.domain.url_to_domain(url)
    password = supergenpass.sgp(passwd, domain, length)
    print "Domain: %s" % domain
    print "Password: %s" % password

if __name__ == "__main__":
    sys.exit(main())
