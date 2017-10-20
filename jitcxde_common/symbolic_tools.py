from symengine.lib.symengine_wrapper import FunctionSymbol

def collect_arguments(expression, function):
	"""
	Parameters
	----------
	expression : SymEngine expression
	function : SymEngine function
	
	Returns
	-------
	arguments : list of SymEngine expressions
		list of all arguments with which `function` is called within `expression`.
	"""
	
	if ( expression.__class__ == FunctionSymbol
			and expression.get_name() == function.name ):
		return {expression.args}
	else:
		return set().union(*(collect_arguments(arg, function) for arg in expression.args))

def ordered_subs(expression,substitutions):
	for substitutions in substitutions:
		expression = expression.subs(*substitution)
	return expression
