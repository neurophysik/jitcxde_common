from itertools import chain
from symengine.printing import ccode
from jitcxde_common.strings import count_up

def codelines(expressions):
	"""
	Tries to convert expressions to working code
	"""
	for expression in expressions:
		try:
			codeline = ccode(expression)
		except RuntimeError as error:
			if "Not supported" not in str(error):
				raise
			else:
				raise NotImplementedError(
						"Cannot convert the following expression to C Code:\n"
						+ str(expression)
					)
		yield codeline + ";\n"

def render_declarator(name, _type, size=0):
	return _type + " " + name + ("[%i]"%size if size else "")

def write_in_chunks(lines,mainfile,deffile,name,chunk_size,arguments,omp=True):
	"""
		Writes lines to files in chunks if appropriate.
		
		Parameters
		----------
		lines: iterator
			the lines of code to be written
		mainfile: file object
			the file that contains the central calls
		deffile: file object
			the file where definitions of functions are included
		name: string
			unique name of what is computed
		chunk_size: integer
			size of chunks. If the number of lines is below this, they will plainly written to mainfile.
		arguments: list of tuples
			Each tuple contains the name, type, and size (optional, for arrays) of an argument needed by the code.
			This is so the arguments can be passed to chunked functions.
		omp: boolean
			whether OMP pragmas should be included
	"""
	funcname = "definitions_" + name
	
	first_chunk = []
	try:
		for _ in range(chunk_size+1):
			first_chunk.append(next(lines))
	except StopIteration:
		# No chunking:
		for line in first_chunk:
			mainfile.write(line)
	else:
		lines = chain(first_chunk, lines)
		
		if omp:
			mainfile.write("#pragma omp parallel sections\n{\n")
		
		while True:
			try:
				next_line = next(lines)
			except StopIteration:
				break
			
			if omp:
				mainfile.write("#pragma omp section\n")
			mainfile.write("{" + funcname + "(")
			deffile.write("void " + funcname + "(")
			if arguments:
				mainfile.write(", ".join(argument[0] for argument in arguments))
				deffile.write(", ".join(render_declarator(*argument) for argument in arguments))
			else:
				deffile.write("void")
			mainfile.write(");}\n")
			deffile.write("){\n")
			
			deffile.write(next_line)
			try:
				for _ in range(chunk_size-1):
					deffile.write(next(lines))
			except StopIteration:
				break
			finally:
				deffile.write("}\n")
			
			funcname = count_up(funcname)
		
		if omp:
			mainfile.write("}")

