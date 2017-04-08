#!/usr/bin/python
# -*- coding: utf-8 -*-

from jitcxde_common.input_handling import sort_helpers
import unittest
from sympy import symbols

class InputHandlingTest(unittest.TestCase):
	def test_sorting(self):
		p, q, r = symbols("p, q, r")
		cyclic_helpers = [ [p,q], [q,r], [r,p] ]
		with self.assertRaises(ValueError):
			sort_helpers(cyclic_helpers)

if __name__ == "__main__":
	unittest.main(buffer=True)


