import sys
import os
import re

contents = os.listdir(os.path.dirname(__file__))
egg_match = re.compile('\.egg$', re.I)
eggs = filter(lambda f: egg_match.search(f) is not None, contents)

for egg in eggs:
	sys.path.insert(0, os.path.join(os.path.dirname(__file__), egg))
