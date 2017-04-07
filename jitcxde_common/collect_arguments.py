from __future__ import print_function, division, with_statement

def collect_arguments(expression, function):
	"""
	Parameters
	----------
	expression : SymPy expression
	function : Sympy function
	
	Returns
	-------
	arguments : list of SymPy expressions
		list of all arguments with which `function` is called within `expression`.
	"""
	
	if expression.__class__ == function:
		return {expression.args}
	else:
		return set().union(*(collect_arguments(arg, function) for arg in expression.args))

