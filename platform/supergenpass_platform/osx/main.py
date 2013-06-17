#!/usr/bin/env python

# SGP Password Generator - Setup
# Copyright (C) 2009 Matt Giuca, Tim Cuthbertson

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

import os, sys
from commands import getstatusoutput
from .. import keyinfo
from ..command import require_command


def notify(domain):
	"""
	Send a system notification that the password has been generated
	"""
	st, output = getstatusoutput("terminal-notifier -group net.gfxmonk.supergenpass -message '%s - password generated' -title 'SuperGenPass'" % domain)
	if st:
		print >> sys.stderr, "(Couldn't show notification)"

def guess_url():
	"""
	Try grabbing the current URL from firefox / safari (whichever is running)
	(this is ugly...)
	For some reason including conditional "tell safari to do blah..." causes safari to open even if that branch
	of code is never even executed. So we're checking which app is open, then doing the conditional logic in python.
	"""
	app_scripts = {
		'firefox': "tell application \"Firefox\" to return (get item 3 of (properties of front window as list))",
		'safari': "tell application \"Safari\" to return (get URL of document 1)",
	}
	
	script = """
		on isRunning(appName)
			tell application "System Events"
				return ((application processes whose (name contains appName)) count) is greater than 0
			end tell
		end isRunning
		"""
	
	for app in app_scripts.keys():
		script += """
		if isRunning("%s") then
			return "%s"
		end if
		""" % (app, app)

	script += "return \"None\""
	# print script
	
	status, output = getstatusoutput("osascript -e '%s'" % script)
	if status != 0 or output == 'None':
		return None
	else:
		app_name = output
		status, output = getstatusoutput("osascript -e '%s'" % app_scripts[app_name])
		if status != 0:
			return None
		# print output
		return output

