from symengine.lib.symengine_wrapper import FunctionSymbol

def is_call(expression,function):
	"""
	whether expression is a call of function
	"""
	return (
			expression.__class__ == FunctionSymbol and
			expression.get_name() == function.name
		)

def function_visitor(expression,function):
	"""
	Generator function that yields all subexpressions of `expression` that are an instance of `function`.
	"""
	
	if is_call(expression,function):
		yield expression
	
	for arg in expression.args:
		yield from function_visitor(arg,function)

def collect_arguments(expression,function):
	"""
	Parameters
	----------
	expression : SymEngine expression
	function : SymEngine function
	
	Returns
	-------
	arguments : set of SymEngine expressions
		set of all arguments with which `function` is called within `expression`.
	"""
	
	return {
			expr.args
			for expr in function_visitor(expression,function)
		}

def count_calls(expression,function):
	"""
	Counts the calls of `function` within `expression`.
	Similar to SymPy’s `count`.
	"""
	return sum(1 for _ in function_visitor(expression,function))

def has_function(expression,function):
	"""
	Checks whether `function` is called within `expression`.
	Similar to SymPy’s `has`.
	"""
	
	try:
		next(function_visitor(expression,function))
	except StopIteration:
		return False
	else:
		return True

def ordered_subs(expression,substitutions):
	for substitution in substitutions:
		expression = expression.subs(*substitution)
	return expression

def replace_function(expression,function,new_function):
	"""
		Replaces all instances of `function` within `expression` with `new_function`.
		To bypass SymEngine issue #1356.
	"""
	if expression.is_Atom:
		return expression
	else:
		replaced_args = (
				replace_function(arg,function,new_function)
				for arg in expression.args
			)
		if is_call(expression,function):
			return new_function(*replaced_args)
		else:
			return expression.func(*replaced_args)

