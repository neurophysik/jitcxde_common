import symengine

class GroupHandler(object):
	def __init__(self,groups):
		self.n = max(max(group) for group in groups)+1
		assert all(all(0<=i<self.n for i in group) for group in groups), "Group elements out of range."
		assert set().union(*groups)==set(range(self.n)), "Groups do not cover all indices."
		assert sum(map(len,groups))==self.n, "Groups overlap."
		
		self.groups = groups
		self._group_finder = None
	
	@property
	def main_indices(self):
		if not hasattr(self,"_main_indices"):
			self._main_indices = map(min,self.groups)
		return self._main_indices
	
	def group_from_index(self,index):
		"""returns the number of the group which contains `i`."""
		
		if self._group_finder is None:
			self.group_finder = {}
			for k,group in enumerate(self.groups):
				for entry in group:
					self.group_finder[entry] = k
		
		return self.group_finder[index]
	
	def iterate(self,iterable):
		"""returns two consecutive elements from `iterable` belonging to the same group. Returns the group index for the first item."""
		
		cache = {}
		for k,entry in enumerate(iterable):
			i = self.group_from_index(k)
			try:
				previous_entry = cache[i]
			except KeyError:
				yield i
			else:
				yield previous_entry,entry
			finally:
				cache[i] = entry
	
	def extract_main(self,iterable):
		"""
		Extracts the elements corresponding to the main indices from `iterable`.

		Returns
		-------
		extractor: generator function
			returns an iterator over iterable
		
		extracted_entries : dictionary
			maps an index of a main component to the corresponding element of `iterable`. Note that this only works once `extractor` has been iterated sufficienly far.
		"""
		
		extracted_entries = {}
		def extractor():
			for i,entry in enumerate(iterable):
				if i in self.main_indices:
					extracted_entries[i] = entry
				yield entry
		return extractor,extracted_entries
	
	def back_transform(self,vector):
		if not hasattr(self,"_A_inv"):
			import sympy
			A = sympy.zeros(self.n,self.n)
			for i,entry in enumerate(self.iterate(range(self.n))):
				if type(entry)==int:
					for j in self.groups[entry]:
						A[i,j]=1
				else:
					A[i,entry[0]] =  1
					A[i,entry[1]] = -1
			
			self._A_inv = symengine.sympify(A.inv())
			
			for j in self.main_indices:
				for i in range(self.n):
					self._A_inv[i,j] = 0
		return self._A_inv*symengine.Matrix(vector)
		
