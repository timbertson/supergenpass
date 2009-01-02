import helper
import eggs
from mocktest import mock_on, mock_wrapper, TestCase

# tested stuff
import commands
import lib.osx.main as osx

class OsxTest(TestCase):
	def test_should_get_password(self):
		def cmd_action(cmd):
			print "** " + cmd
			if 'list-keychains' in cmd:
				return (0,'"login/login.keychain"')
			return (0,'"acct"<blob>="foo"\npassword: "blah"')
		
		cmd = mock_on(commands).getstatusoutput.with_action(cmd_action)
		self.assertEqual(osx.get_password(False), 'blah')
	
	def test_should_ask_for_password_if_getting_fails(self):
		keychain = mock_on(osx).Keychain
		def raiseit(*args):
			raise osx.keychainError
		keychain.child('password').action = raiseit
		mock_on(osx.globals())

