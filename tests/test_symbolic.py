import unittest
from symengine import Function, Symbol, sin, Integer
from jitcxde_common.symbolic import collect_arguments, count_calls, has_function, replace_function, conditional

f = Function("f")
g = Function("g")
a = Symbol("a")

class TestCollectArguments(unittest.TestCase):
	def test_complex_expression(self):
		expression = 3**f(42) + 23 - f(43,44) + f(45+a)*sin( g(f(46,47,48)+17) - g(4) ) + sin(f(42))
		
		self.assertEqual(
				collect_arguments(expression,f),
				{
					(Integer(42),),
					(Integer(43), Integer(44)),
					(45+a,),
					(Integer(46), Integer(47), Integer(48))
				}
			)
		
		self.assertEqual(count_calls(expression,f),5)
		self.assertTrue(has_function(expression,f))
		self.assertEqual(
				replace_function(expression,f,g),
				3**g(42) + 23 - g(43,44) + g(45+a)*sin( g(g(46,47,48)+17) - g(4) ) + sin(g(42))
			)
	
	def test_function_within_function(self):
		expression = f(f(42))
		
		self.assertEqual(
				collect_arguments(expression, f),
				{ (Integer(42),) , (f(Integer(42)),) }
			)
		
		self.assertEqual(count_calls(expression,f),2)
		self.assertTrue(has_function(expression,f))
		self.assertEqual( replace_function(expression,f,g), g(g(42)) )
	
	def test_no_function(self):
		expression = g(a)+42
		
		self.assertEqual( collect_arguments(expression,f), set() )
		self.assertEqual(count_calls(expression,f),0)
		self.assertFalse(has_function(expression,f))
		self.assertEqual( replace_function(expression,f,g), g(a)+42 )

ε = 1e-2
conditional_test_cases = [
		( 41  , 42,  7, 23,  7 ),
		( 42-ε, 42,  7, 23,  7 ),
		( 42  , 42,  7, 23, 15 ),
		( 42+ε, 42,  7, 23, 23 ),
		( 43  , 42,  7, 23, 23 ),
		( 41  , 42, 23,  7, 23 ),
		( 42-ε, 42, 23,  7, 23 ),
		( 42  , 42, 23,  7, 15 ),
		( 42+ε, 42, 23,  7,  7 ),
		( 43  , 42, 23,  7,  7 ),
		( -1  ,  0,  7, 23,  7 ),
		(   -ε,  0,  7, 23,  7 ),
		(  0  ,  0,  7, 23, 15 ),
		(   +ε,  0,  7, 23, 23 ),
		(  1  ,  0,  7, 23, 23 ),
	]

class TestConditional(unittest.TestCase):
	def test_number_input(self):
		for obs,thr,v_if,v_else,result in conditional_test_cases:
			self.assertAlmostEqual(
					float(conditional(obs,thr,v_if,v_else)),
					result,
				)
	
	def test_symbolic_threshold(self):
		for obs,thr,v_if,v_else,result in conditional_test_cases:
			self.assertAlmostEqual(
					float(conditional(obs,a,v_if,v_else).subs({a:thr})),
					result,
				)
	
	def test_wide_width(self):
		self.assertNotAlmostEqual(
				float(conditional(1,0,-1,1,width=1e5)),
				1,
			)

if __name__ == "__main__":
	unittest.main(buffer=True)
