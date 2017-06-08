from __future__ import print_function, division, with_statement
from inspect import isgeneratorfunction
from sympy import sympify

def handle_input(f_sym,n):
	"""
	Converts f_sym to a generator function, if necessary.
	Ensures that n is the length of f_sym, if not predefined.
	"""
	if isgeneratorfunction(f_sym):
		n = n or sum(1 for _ in f_sym())
		return f_sym, n
	elif len(f_sym) == 0:
		return lambda:f_sym, n
	else:
		len_f = len(f_sym)
		if (n is not None) and (len_f != n):
			raise ValueError("len(f_sym) and n do not match.")
		return (lambda: (entry.doit() for entry in f_sym)), len_f

def depends_on_any(helper, other_helpers):
	for other_helper in other_helpers:
		if helper[1].has(other_helper[0]):
			return True
	return False

def sort_helpers(helpers):
	"""
	sorts a list of helpers such that no helper depends on a later one.
	"""
	
	if len(helpers)>1:
		for j,helper in enumerate(helpers):
			if not depends_on_any(helper, helpers):
				helpers.insert(0,helpers.pop(j))
				break
		else:
			raise ValueError("Helpers have cyclic dependencies.")
		
		helpers[1:] = sort_helpers(helpers[1:])
	
	return helpers

def sympify_helpers(helpers):
	return [(helper[0], sympify(helper[1]).doit()) for helper in helpers]

def filter_helpers(helpers,symbols):
	"""
	filters a list of helpers to contain only those listed in symbols and those needed for calculating them.
	"""
	needed = set(symbols) # convert and copy
	
	filtered_rev = []
	for helper in reversed(helpers):
		if helper[0] in needed:
			filtered_rev.append(helper)
			needed.update(helper[1].free_symbols)
	
	return list(reversed(filtered_rev))

def copy_helpers(helpers):
	return [helper for helper in helpers]

