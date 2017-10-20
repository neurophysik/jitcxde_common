import unittest
from symengine import Function, Symbol, sin, Integer
from jitcxde_common.symbolic_tools import collect_arguments

class TestCollectArguments(unittest.TestCase):
	def test_complex_expression(self):
		f = Function("f")
		g = Function("g")
		a = Symbol("a")
		
		expression = 3**f(42) + 23 - f(43,44) + f(45+a)*sin( g(f(46,47,48)+17) - g(4) )
		
		self.assertEqual(
			collect_arguments(expression, f),
			{
				(Integer(42),),
				(Integer(43), Integer(44)),
				(45+a,),
				(Integer(46), Integer(47), Integer(48))}
			)

if __name__ == "__main__":
	unittest.main(buffer=True)
