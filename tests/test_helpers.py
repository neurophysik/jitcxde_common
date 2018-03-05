#!/usr/bin/python3
# -*- coding: utf-8 -*-

from jitcxde_common.helpers import sort_helpers, filter_helpers, copy_helpers, find_dependent_helpers
import unittest
from symengine import symbols, sin, cos, Integer
from itertools import permutations

p,q,r,s,u,v = symbols("p q r s u v")

cycle = [ [p,q], [q,r], [r,p] ]
chain = [ [r,s], [q,r], [p,q] ]

class SortingTest(unittest.TestCase):
	def test_cyclic(self):
		for permutation in permutations(cycle):
			with self.assertRaises(ValueError):
				sort_helpers(permutation)
	
	def test_sorting(self):
		for permutation in permutations(chain):
			result = sort_helpers(list(permutation))
			assert result==chain

class FilterTest(unittest.TestCase):
	def test_all_needed(self):
		assert chain==filter_helpers(chain,{p})
	
	def test_spurious(self):
		chain_with_spurious = chain+[[u,v]]
		assert chain==filter_helpers(chain_with_spurious,{p})

class CopyTest(unittest.TestCase):
	def test_copy(self):
		assert chain==copy_helpers(chain)
	
	def test_independence(self):
		copy = copy_helpers(chain)
		copy.append([u,v])
		assert copy!=chain

class FindDependentTest(unittest.TestCase):
	def test_find_dependent_helpers(self):
		helpers = [
				( q, p           ),
				( r, sin(q)      ),
				( s, 3*p+r       ),
				( u, Integer(42) ),
			]
		control = [
				( q, 1        ),
				( r, cos(q)   ),
				( s, 3+cos(q) ),
			]
		dependent_helpers = find_dependent_helpers(helpers,p)
		# This check is overly restrictive due to depending on the order and exact form of the result:
		self.assertListEqual(dependent_helpers,control)

if __name__ == "__main__":
	unittest.main(buffer=True)


