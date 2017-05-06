from __future__ import print_function, division, with_statement
from sympy import preorder_traversal

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
	
	arguments = set()
	for subexpression in preorder_traversal(expression):
		if subexpression.__class__ == function:
			arguments.add(subexpression.args)
	return arguments
