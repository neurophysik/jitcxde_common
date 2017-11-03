import unittest
from jitcxde_common.transversal import GroupHandler

class TestFinderAndIterator(unittest.TestCase):
	def test_ordered_groups(self):
		groups = [ [0,1,2], [3,4,5] ]
		G = GroupHandler(groups)
		
		for i in range(6):
			self.assertIn(i,groups[G.group_from_index(i)])
		
		sequence = list(G.iterate(range(6)))
		expected = [
				  0  ,
				(0,1),
				(1,2),
				  1  ,
				(3,4),
				(4,5)
			]
		self.assertSequenceEqual(sequence,expected)
	
	def test_alternating_groups(self):
		groups = [ [0,2,4], [1,3,5] ]
		G = GroupHandler(groups)
		sequence = list(G.iterate(range(6)))
		expected = [
				  0  ,
				  1  ,
				(0,2),
				(1,3),
				(2,4),
				(3,5)
			]
		self.assertSequenceEqual(sequence,expected)

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
