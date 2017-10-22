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
	
	result = set()
	
	if ( expression.__class__ == FunctionSymbol
			and expression.get_name() == function.name ):
		result.add(expression.args)
	
	for arg in expression.args:
		result.update( collect_arguments(arg,function) )
	
	return result

def count_calls(expression,function):
	"""
	Counts the calls of `function` within `expression`.
	Similar to SymPy’s `count`.
	"""
	result = 0
	
	if ( expression.__class__ == FunctionSymbol
			and expression.get_name() == function.name ):
		result += 1
	
	result += sum( count_calls(arg,function) for arg in expression.args )
	
	return result

def has_function(expression,function):
	"""
	Checks whether `function` is called within `expression`.
	Similar to SymPy’s `has`.
	"""
	
	if ( expression.__class__ == FunctionSymbol
			and expression.get_name() == function.name ):
		return True
	
	for arg in expression.args:
		if has_function(arg,function):
			return True
	
	return False

def ordered_subs(expression,substitutions):
	for substitution in substitutions:
		expression = expression.subs(*substitution)
	return expression

