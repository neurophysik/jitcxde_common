#!/usr/bin/python
# -*- coding: utf-8 -*-

from jitcxde_common.strings import remove_suffix, ensure_suffix, count_up
import unittest

class StringTest(unittest.TestCase):
	def test_remove_suffix(self):
		self.assertEqual( remove_suffix("foo.so", ".so"), "foo" )
		self.assertEqual( remove_suffix("foo.sob", ".so"), "foo.sob" )
		self.assertEqual( remove_suffix("foo.xy", ".so"), "foo.xy" )
	
	def test_ensure_suffix(self):
		self.assertEqual( ensure_suffix("foo", ".so"), "foo.so" )
		self.assertEqual( ensure_suffix("foo.so", ".so"), "foo.so" )
		self.assertEqual( ensure_suffix("foo.sob", ".so"), "foo.sob.so" )
		
	def test_count_up(self):
		self.assertEqual( count_up("foo"), "foo_1" )
		self.assertEqual( count_up("foo_2"), "foo_3" )
		self.assertEqual( count_up("foo_9"), "foo_10" )
		self.assertEqual( count_up("foo_009"), "foo_010" )
		self.assertEqual( count_up("foo_0"), "foo_1" )

if __name__ == "__main__":
	unittest.main(buffer=True)


