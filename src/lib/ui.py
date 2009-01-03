import sys
def get_input(prompt):
	try:
		return raw_input(prompt)
	except (EOFError, KeyboardInterrupt):
		print
		sys.exit(2)

