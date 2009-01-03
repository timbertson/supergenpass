# make ../src available
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# make system eggs available
import eggloader


