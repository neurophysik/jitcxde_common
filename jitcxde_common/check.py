# This creates an infrastructure for checks for JiTC*DE objects that works as follows:
# • Each check is registered as such by being decorated with `@checker`.
# • Each class that needs checks inherits from CheckEnvironment.
# • All checks are run with the method check.

# This class exist just to mark functions
class CheckerWrapper(object):
	def __init__(self,function):
		self.function = function
	
	def __call__(self,*args):
		self.function(*args)

# Decorator for checks
def checker(function):
	return CheckerWrapper(function)

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
				if name not in visited and isinstance(member,CheckerWrapper):
					member(self)
				visited.add(name)
		
		if self.failed_check:
			raise ValueError("Check failed.")

