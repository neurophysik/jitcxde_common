import unittest
from jitcxde_common.transversal import GroupHandler

class TestOrdered(unittest.TestCase):
	@classmethod
	def setUpClass(self):
		self.n = 6
		self.groups = [ [0,1,2], [3,4,5] ]
		self.main_indices = [0,3]
		self.iteration = [ 0 , (0,1), (1,2), 1 , (3,4), (4,5) ]
	
	def setUp(self):
		self.G = GroupHandler(self.groups)
	
	def test_group_from_index(self):
		for i in range(self.n):
			self.assertIn(i,self.groups[self.G.group_from_index(i)])
	
	def test_iterate(self):
		self.assertSequenceEqual(
				list(self.G.iterate(range(self.n))),
				self.iteration
			)
		
	def test_main_indices(self):
		self.assertSequenceEqual(
				list(self.G.main_indices),
				self.main_indices
			)
	
	def test_extractor(self):
		original = range(100,100+self.n)
		extractor,extracted = self.G.extract_main(original)
		sequence = list(extractor())
		self.assertSequenceEqual(sequence,original)
		for i in self.G.main_indices:
			self.assertEqual(extracted[i],original[i])

class TestAlternating(unittest.TestCase):
	@classmethod
	def setUpClass(self):
		self.groups = [ [0,2,4], [1,3,5] ]
		self.main_indices = [0,1]
		self.iteration = [ 0 , 1 , (0,2), (1,3), (2,4), (3,5) ]

class TestErrors(unittest.TestCase):
	def test_missing_indices(self):
		groups = [(0,1),(3,4)]
		with self.assertRaises(AssertionError):
			GroupHandler(groups)
	
	def test_duplicte_indices(self):
		groups = [(0,1),(1,2,3,4)]
		with self.assertRaises(AssertionError):
			GroupHandler(groups)

if __name__ == "__main__":
	unittest.main(buffer=True)

