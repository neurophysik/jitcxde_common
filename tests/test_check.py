import unittest
from jitcxde_common.check import CheckEnvironment, checker

class SomeChecks(CheckEnvironment):
	def __init__(self,fail=True):
		self.invoked = []
		self.fail = fail
	
	@checker
	def A(self):
		self.invoked.append(1)
	
	@checker
	def B(self):
		self.invoked.append(2)
		self._check_assert( not self.fail, "Check A failed." )
	
	@checker
	def C(self):
		self.invoked.append(3)
	
	@checker
	def D(self):
		self.invoked.append(4)
		self._check_assert( not self.fail, "Check D failed." )

	def E(self):
		raise AssertionError("This method should not be run")

class DifferentChecks(SomeChecks):
	def A(self):
		raise AssertionError("This method should not be run")
	
	@checker
	def B(self):
		self.invoked.append(5)
	
	@checker
	def C(self):
		self.invoked.append(6)
		self._check_assert( not self.fail, "Check C failed." )

class TestChecks(unittest.TestCase):
	def test_default(self):
		X = SomeChecks(fail=True)
		with self.assertRaises(ValueError):
			X.check()
		assert (2 in X.invoked) ^ (4 in X.invoked)
	
	def test_fail_slow(self):
		X = SomeChecks(fail=True)
		with self.assertRaises(ValueError):
			X.check(fail_fast=False)
		self.assertListEqual( sorted(X.invoked), [1,2,3,4] )
	
	def test_success(self):
		X = SomeChecks(fail=False)
		X.check()
		self.assertListEqual( sorted(X.invoked), [1,2,3,4] )

class TestInheritance(unittest.TestCase):
	def test_default(self):
		X = DifferentChecks(fail=True)
		with self.assertRaises(ValueError):
			X.check()
		assert (4 in X.invoked) ^ (6 in X.invoked)
		assert all( i not in X.invoked for i in [1,2,3] )
	
	def test_fail_slow(self):
		X = DifferentChecks(fail=True)
		with self.assertRaises(ValueError):
			X.check(fail_fast=False)
		self.assertListEqual( sorted(X.invoked), [4,5,6] )
	
	def test_success(self):
		X = DifferentChecks(fail=False)
		X.check()
		self.assertListEqual( sorted(X.invoked), [4,5,6] )

if __name__ == "__main__":
	unittest.main(buffer=True)

