#!/usr/bin/python3
# -*- coding: utf-8 -*-

from jitcxde_common.strings import count_up
import unittest

class StringTest(unittest.TestCase):
	def test_count_up(self):
		self.assertEqual( count_up("foo"), "foo_1" )
		self.assertEqual( count_up("foo_2"), "foo_3" )
		self.assertEqual( count_up("foo_9"), "foo_10" )
		self.assertEqual( count_up("foo_009"), "foo_010" )
		self.assertEqual( count_up("foo_0"), "foo_1" )

if __name__ == "__main__":
	unittest.main(buffer=True)


