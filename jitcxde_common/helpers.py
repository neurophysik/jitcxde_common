from symengine import sympify

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
	return [(sympify(helper[0]), sympify(helper[1])) for helper in helpers]

def filter_helpers(helpers,symbols):
	"""
	filters a list of helpers to contain only those listed in `symbols` and those needed for calculating them.
	"""
	needed = set(symbols) # convert and copy
	filtered_rev = []
	for helper in reversed(helpers):
		if helper[0] in needed:
			filtered_rev.append(helper)
			needed.update(helper[1].free_symbols)
	
	return list(reversed(filtered_rev))

def find_dependent_helpers(helpers,dependency):
	"""
	Returns a list of helpers depending on `dependency` and their respective derivative (applying the chain rule).
	"""
	
	dependent_helpers = []
	
	for helper in helpers:
		derivative = sum(
				(
					helper[1].diff(other_helper[0]) * other_helper[1]
					for other_helper in dependent_helpers
				),
				helper[1].diff(dependency)
			)
		if derivative != 0:
			dependent_helpers.append( (helper[0], derivative) )
	
	return dependent_helpers

def copy_helpers(helpers):
	return [helper for helper in helpers]

