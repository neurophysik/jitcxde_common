class GroupHandler(object):
	def __init__(self,groups):
		self.groups = groups
		self._group_finder = None
	
	def group_from_index(self,index):
		"""returns the number of the group which contains `i`."""
		
		if self._group_finder is None:
			self.group_finder = {}
			for k,group in enumerate(self.groups):
				for entry in group:
					self.group_finder[entry] = k
		
		return self.group_finder[index]
	
	def iterate(self,generator):
		"""returns two consecutive elements from `generator` belonging to the same group. Returns the group index for the first item."""
		
		cache = {}
		for k,entry in enumerate(generator):
			i = self.group_from_index(k)
			try:
				previous_entry = cache[i]
			except KeyError:
				yield i
			else:
				yield previous_entry,entry
			finally:
				cache[i] = entry
		
