# A temporary measure to ensure that nobody tries to run this with an insufficient SymEngine version. If I could just check the version number, this issue wouldn’t exist in the first place.

def symengine_check():
	from symengine.printing import ccode
	from symengine import Symbol, Function
	
	f = Function("f")
	x = Symbol("x")
	
	# If this fails, there is more wrong than just the SymEngine version:
	ccode(x)
	
	# If this fails (and the above doesn’t), it’s almost certainly the SymEngine version:
	try:
		ccode(f(x))
	except RuntimeError:
		raise NotImplementedError("""
===============================================
READ ME FIRST

Your version of SymEngine is too low. Unless a new version of SymEngine was released recently (see https://github.com/symengine/symengine.py/issues/204), you can only address this by building SymEngine from source. See http://jitcde-common.readthedocs.io/#building-from-source for instructions.
===============================================
		""")

