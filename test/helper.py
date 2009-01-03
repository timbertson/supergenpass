# make ../src available
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# make mocktest available
import eggloader
eggloader.load('mocktest')

