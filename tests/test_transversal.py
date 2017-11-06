import unittest
import symengine
from jitcxde_common.transversal import GroupHandler

class TestOrdered(unittest.TestCase):
	@classmethod
	def setUpClass(self):
		self.n = 6
		self.groups = [ [0,1,2], [3,4,5] ]
		self.main_indices = [0,3]
		self.tangent_indices = [1,2,4,5]
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
	
	def test_tangent_indices(self):
		self.assertCountEqual(
				list(self.G.tangent_indices),
				self.tangent_indices
			)
	
	def test_extractor(self):
		original = range(100,100+self.n)
		extractor,extracted = self.G.extract_main(lambda:original)
		sequence = list(extractor())
		self.assertSequenceEqual(sequence,original)
		for i in self.G.main_indices:
			self.assertEqual(extracted[i],original[i])
	
	def test_back_transform(self):
		z = symengine.Function("z")
		
		z_v = [z(i) for i in range(self.n)]
		y_v = self.G.back_transform(z_v)
		
		transformed = []
		for entry in self.G.iterate(range(self.n)):
			if type(entry)==int:
				transformed.append( sum(y_v[i] for i in self.groups[entry]) )
			else:
				transformed.append( y_v[entry[0]] - y_v[entry[1]] )
		
		for i in self.G.main_indices:
			z_v[i] = 0
		self.assertSequenceEqual(
				z_v,
				[entry.simplify() for entry in transformed]
			)

class TestAlternating(TestOrdered):
	@classmethod
	def setUpClass(self):
		self.n = 6
		self.groups = [ [0,2,4], [1,3,5] ]
		self.main_indices = [0,1]
		self.tangent_indices = [2,3,4,5]
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

