SGP Password Generator
Portions Copyright (C) Chris Zarate
Portions Copyright (C) 2008-2009 Matt Giuca, Tim Cuthbertson

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License version 2,
as published by the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

About
=====

Reference implementation of the SuperGenPass algorithm in Python. Ported from
http://supergenpass.com/. This tool generates a unique password for each
domain, solving the problem of having to remember a million passwords.

SuperGenPass (http://supergenpass.com/) is a JavaScript bookmarklet tool for
generating a password based on a hash of your master password, and some domain
name. This means you can generate a unique password for each website you use,
solving the problem of one bad site getting your main password. But, you don't
need to remember anything but your master password.

We have ported it to Python for a number of reasons:

* We want a clearly readable reference implementation of the algorithm, so we
  know how it works and we can trust it.
* We want to use the tool in a number of forms: on the command line, in a GUI,
  integrated with the operating system, on mobile devices, etc. Python is
  widely used and can produce tools in all these forms and more.
* There is a subtle security vulnerability in the JavaScript bookmarklet
  version -- a malicious site could snoop the master password from the
  JavaScript form. This vulnerability is not present in offline versions of
  the algorithm (though this is also true of the "mobile version" provided at
  http://supergenpass.com/mobile/).

PySGP is that implementation. It should generate the exact same passwords as
SuperGenPass 1.3, so you can use the two tools interchangeably. We would like
to further this by developing a more rigorous specification of the SGP
algorithm, which can be implemented by many tools in a compatible way.

We are currently getting ourselves set up, so there is not a lot of
documentation. This tool is in its early stages, so please don't rely on it -
use the JavaScript version. If you want to help us out, use our tool as well
as the original JavaScript one, and let us know if there are any discrepancies
between the two.

Directory hierarchy
===================

The source tree is arranged as follows:

* src/ - All source code.
* src/sgp - The basic sgp command-line program.
* src/supergenpass/ - The core supergenpass Python package (for installation
    into site-packages).
* src/supergenpass_platform/ - The "platform integration" component, which uses
    platform-specific code to integrate with various operating systems.
    All platform-specific code should be in this directory.

OS X integration
================

* works with firefox or safari to get the current URL if you don't specify one
* uses the OSX keychain service to get/save your master password

keychain (osx): https://launchpad.net/keychain.py/

Linux integration (gnome only, currently)
=========================================

* works with firefox to get the current URL if you don't specify one (requires
  the "mozRepl" firefox extension to be installed and running)
* uses the gnomekeyring service to get/save your master password
* requires "xsel" (debian package) to copy password to the clipboard

keyring (gnome): http://www.rittau.org/blog/20070726-01
