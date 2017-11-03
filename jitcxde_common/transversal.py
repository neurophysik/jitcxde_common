class GroupHandler(object):
	def __init__(self,groups):
		n = max(max(group) for group in groups)+1
		assert all(all(0<=i<n for i in group) for group in groups), "Group elements out of range."
		assert set().union(*groups)==set(range(n)), "Groups do not cover all indices."
		assert sum(map(len,groups))==n, "Groups overlap."
		
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
		
