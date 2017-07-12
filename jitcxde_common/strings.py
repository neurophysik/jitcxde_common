from __future__ import print_function, division, with_statement

# String manipulation
# -------------------

# obsolete
def remove_suffix(string, suffix):
	partition = string.rpartition(suffix)
	if partition[1] and not partition[2]:
		return partition[0]
	else:
		return string

# obsolete
def ensure_suffix(string, suffix):
	if not string.endswith(suffix):
		return string + suffix
	else:
		return string

def rsplit_int(s):
	if s and s[-1].isdigit():
		x,y = rsplit_int(s[:-1])
		return x, y+s[-1]
	else:
		return s, ""

def count_up(name):
	s, i = rsplit_int(name)
	return s + ( "%%.%ii" % len(i) % (int(i)+1)  if i else "_1" )

