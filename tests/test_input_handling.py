#!/usr/bin/python
# -*- coding: utf-8 -*-

from jitcxde_common.input_handling import sort_helpers, filter_helpers, copy_helpers
import unittest
from sympy import symbols
from itertools import permutations
from sympy.abc import p,q,r,s,u,v

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

if __name__ == "__main__":
	unittest.main(buffer=True)


