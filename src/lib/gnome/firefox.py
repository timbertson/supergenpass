import commands
import os

from ..command import require_command

def guess_url():
	require_command('expect', package='expect')
	fresno = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fresno')
	(status, output) = commands.getstatusoutput('\'%s\' -j content.location.href' % (fresno,))
	if status != 0:
		raise OSError("fresno failed with output: %s\n" % (output) + 
		              "make sure you have installed mozRepl and it is turned on\n" + 
		              "(http://github.com/bard/mozrepl/wikis/home)")
	return output

