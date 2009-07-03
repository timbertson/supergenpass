# make ../src available
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..','supergenpass_platform'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..','supergenpass'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import eggloader
