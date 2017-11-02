
def group_finder(groups):
	"""returns a dictionary that maps each entry to the index of the group in which it is contained"""
	
	result = {}
	for k,group in enumerate(groups):
		for entry in group:
			result[entry] = k
	return result

def group_handler(groups,generator):
	"""returns two consecutive elements from `generator` belonging to the same group. Returns the group index for the first item."""
	
	finder = group_finder(groups)
	cache = {}
	for k,entry in enumerate(generator):
		i = finder[k]
		try:
			previous_entry = cache[i]
		except KeyError:
			yield i
		else:
			yield previous_entry,entry
		finally:
			cache[i] = entry
	
