import user
import os

domain_filename = '.supergenpass.domains'

def remember(domain):
	domains = get_domains()
	if not domain in domains:
		domains.append(domain)
		set_domains(sorted(domains))

def forget(domain):
	domains = get_domains()
	if domain in domains:
		domains.remove(domain)
		set_domains(sorted(domains))
	
## implementation ##

def unique(lst):
	return list(set(lst))

def read_file_lines(filename):
	f = open(filename)
	lines = [line.strip() for line in f.readlines()]
	f.close()
	return unique(lines)

def write_file_lines(filename, lines):
	f = open(filename, 'w')
	f.writelines('\n'.join(lines))
	f.write('\n')
	f.close()

def get_domain_file():
	return os.path.join(user.home, domain_filename)

def get_domains():
	try:
		return read_file_lines(get_domain_file())
	except IOError:
		return []

def set_domains(domains):
	write_file_lines(get_domain_file(), domains)

