import unittest
from jitcxde_common.transversal import group_handler

class TestGroupFinder(unittest.TestCase):
	def test_ordered_groups(self):
		groups = [ [0,1,2], [3,4,5] ]
		handler = group_handler(groups,range(6))
		expected = [
				  0  ,
				(0,1),
				(1,2),
				  1  ,
				(3,4),
				(4,5)
			]
		self.assertSequenceEqual(list(handler),expected)
	
	def test_alternating_groups(self):
		groups = [ [0,2,4], [1,3,5] ]
		handler = group_handler(groups,range(6))
		expected = [
				  0  ,
				  1  ,
				(0,2),
				(1,3),
				(2,4),
				(3,5)
			]
		self.assertSequenceEqual(list(handler),expected)


if __name__ == "__main__":
	unittest.main(buffer=True)
