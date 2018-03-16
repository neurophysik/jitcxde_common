#!/usr/bin/python3
# -*- coding: utf-8 -*-

from inspect import isfunction

# Decorator for checks
def checker(function):
	function._is_checker = True
	return function

class CheckEnvironment(object):
	def _check_assert(self,condition,message):
		if not condition:
			self.failed_check = True
			if self.fail_checks_fast:
				raise ValueError(message)
			else:
				print(message)
	
	def check(self, fail_fast=True):
		"""
		Performs a series of checks that may not be feasible at runtime (usually due to their length). Whenever you run into an error that you cannot make sense of, try running this. It checks for the following mistakes:
		
		* negative arguments of `y`
		* arguments of `y` that are higher than the system’s dimension `n`
		* unused variables
		
		Parameters
		----------
		fail_fast : boolean
			whether to abort on the first failure. If false, an error is raised only after all problems are printed.
		"""
		
		self.failed_check = False
		self.fail_checks_fast = fail_fast
		
		# execute all methods decorated with checker:
		visited = set()
		for cls in [self.__class__] + self.__class__.mro():
			for name,member in cls.__dict__.items():
				if (
						    name not in visited
						and not isinstance(member,property)
						and isfunction(member)
						and hasattr(member,"_is_checker")
						and member._is_checker
					):
						member(self)
				visited.add(name)
		
		if self.failed_check:
			raise ValueError("Check failed.")

