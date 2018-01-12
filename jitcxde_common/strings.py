def rsplit_int(s):
	"""
	splits off the largest substring of digits from the right a string
	"""
	if s and s[-1].isdigit():
		x,y = rsplit_int(s[:-1])
		return x, y+s[-1]
	else:
		return s, ""

def count_up(name):
	"""
	If `name` ends on a number, increase that number by one. Otherwise append “_1”.
	"""
	s, i = rsplit_int(name)
	return s + ( "%%.%ii" % len(i) % (int(i)+1)  if i else "_1" )

