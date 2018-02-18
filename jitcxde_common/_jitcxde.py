#!/usr/bin/python3
# -*- coding: utf-8 -*-

from tempfile import mkdtemp
from os import path
from inspect import stack, isgeneratorfunction
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import shutil
from sys import modules
from warnings import warn
from traceback import format_exc

import numpy
from jinja2 import Environment, FileSystemLoader
from symengine import sympify

from jitcxde_common.modules import get_module_path, modulename_from_path, find_and_load_module, module_from_path, add_suffix
from jitcxde_common.strings import count_up
from jitcxde_common.code import write_in_chunks, codelines

#: A list with the default extra compile arguments. Note that without `-Ofast`, `-ffast-math`, or `-funsafe-math-optimizations` (if supported by your compiler), you may experience a considerable speed loss since SymEngine uses the `pow` function for small integer powers (cf. `SymPy Issue 8997`_).
DEFAULT_COMPILE_ARGS = [
			"-std=c11",
			"-Ofast",
			"-g0",
			"-march=native",
			"-mtune=native",
			"-Wno-unknown-pragmas",
			]

#: A list with the default linker arguments.
DEFAULT_LINK_ARGS = [ "-lm" ]

#: A list with the default compile arguments for the Microsoft compiler. I could not find what level of optimisation is needed to address the problem of SymEngine using the `pow` function for small integer powers (`SymPy Issue 8997`_).
MSVC_COMPILE_ARGS = [
			"/Ox",
			"/wd4068",
			"/wd4146",
			"/wd4018"
			]

#: A list with the default linker arguments for the Microsoft compiler.
MSVC_LINK_ARGS = [ "/ignore:4197" ]

class jitcxde(object):
	"""
	A base class containing elementary, common functionalities of all JiTC*DE projects – mostly file and input handling. It is pretty dysfunctional on its own and only made to be inherited from.
	"""
	
	def __init__(self,n=None,verbose=True,module_location=None):
		self._tmpdir = None
		self.verbose = verbose
		self._modulename = "jitced"
		self.n = n
		
		if module_location is not None:
			self.jitced = module_from_path(module_location)
			self.compile_attempt = True
		else:
			self.jitced = None
			self.compile_attempt = None
		
		# self.compile_attempt is:
		#	• None if no compile attempt was made
		#	• False if a compile attempt was made but not succesful
		#	• True if a successful compile attempt was made
	
	def _handle_input(self,f_sym,n_basic=False):
		"""
		Converts f_sym to a generator function if necessary.
		Ensures that self.n (or self.n_basic) is the length of f_sym if not predefined.
		Ensures that entries are SymPy expressions.
		"""
		
		n = self.n_basic if n_basic else self.n
		
		if isgeneratorfunction(f_sym):
			length = n or sum(1 for _ in f_sym())
		else:
			length = len(f_sym) or n
			# (allowing 0-length f_syms for testing purposes only)
		
		if n is not None and length != n:
			raise ValueError("len(f_sym) and n do not match.")
		
		if n_basic: self.n_basic = length
		else:       self.n       = length
		
		def new_f_sym():
			gen = f_sym() if isgeneratorfunction(f_sym) else f_sym
			for entry in gen:
				yield sympify(entry)
		
		return new_f_sym
	
	def _tmpfile(self,filename=None):
		"""
			returns the path to a file in the tempory directory associated to this instance or the directory itself (if `filename` is None). Creates the directory if necessary.
		"""
		if self._tmpdir is None:
			self._tmpdir = mkdtemp()
		
		if filename is None:
			return self._tmpdir
		else:
			return path.join(self._tmpdir, filename)
	
	def report(self,message):
		if self.verbose:
			print(message)
	
	def _process_modulename(self,modulename):
		"""
		Sets the modulename from input (if specified) or automatically.
		"""
		if modulename:
			if modulename in modules.keys():
				raise NameError("Module name has already been used in this instance of Python.")
			self._modulename = modulename
		else:
			while self._modulename in modules.keys():
				self._modulename = count_up(self._modulename)
		
		modulefile = self._tmpfile(self._modulename + ".so")
		if path.isfile(modulefile):
			raise OSError("Module file already exists.")
	
	@property
	def sourcefile(self):
		return self._tmpfile(self._modulename + ".c")
	
	def _render_template(self,**kwargs):
		"""
		use Jinja2 to render a template for the module
		"""
		kwargs["module_name"] = self._modulename
		folder = path.dirname( stack()[1][1] )
		env = Environment(loader=FileSystemLoader(folder))
		template = env.get_template("jitced_template.c")
		with open(self.sourcefile, "w") as codefile:
			codefile.write(template.render(kwargs))
	
	def render_and_write_code(self,
			expressions,
			name,
			chunk_size = 100,
			arguments = (),
			omp = True,
			):
		"""
			Writes expressions to code.
			
			Parameters
			----------
			expressions: iterator
				expressions to be written
			name: string
				unique name of what is computed
			chunk_size: integer
				size of chunks. If smaller than 1, no chunking happens.
			arguments: list of tuples
				Each tuple contains the name, type, and size (optional, for arrays) of an argument needed by the code.
				This is so the arguments can be passed to chunked functions.
			omp: boolean
				whether OMP pragmas should be included
		"""
		
		with \
				open( self._tmpfile(name+".c"            ), "w" ) as mainfile, \
				open( self._tmpfile(name+"_definitions.c"), "w" ) as deffile:
			if chunk_size < 1:
				for line in codelines(expressions):
					mainfile.write(line)
			else:
				write_in_chunks(
						codelines(expressions),
						mainfile,
						deffile,
						name,
						chunk_size,
						arguments,
						omp
					)

	def _attempt_compilation(self,reset=True):
		self.report("Generating, compiling, and loading C code.")
		try:
			self.compile_C()
		except:
			warn(format_exc())
			line = "\n"+60*"="+"\n"
			warn(line + "READ ME FIRST" + line + "Generating compiled integrator failed; resorting to lambdified functions. If you can live with using the Python backend, you can call generate_lambdas to explicitly do this and bypass the compile attempt and error messages. Otherwise, you want to take care of fixing the above errors." + 2*line)
		else:
			if reset:
				self.reset_integrator()
	
	def _compile_and_load(self,
				verbose,
				extra_compile_args,
				extra_link_args = None,
				omp = False,
			):
		
		extension = Extension(
				self._modulename,
				sources = [self.sourcefile],
				include_dirs = [numpy.get_include()],
			)
		
		script_args = [
				"build_ext",
				"--build-lib", self._tmpfile(),
				"--build-temp", self._tmpfile(),
				"--force",
			]
		
		if not omp:
			omp = ( [], [] )
		elif omp is True:
			omp = ( ["-fopenmp"], ["-lomp"] )
		
		def determine_compile_args(is_msvc):
			if extra_compile_args is None:
				if is_msvc:
					return omp[0] + MSVC_COMPILE_ARGS
				else:
					return omp[0] + DEFAULT_COMPILE_ARGS
			else:
				return omp[0] + extra_compile_args
		
		def determine_link_args(is_msvc):
			if extra_link_args is None:
				if is_msvc:
					return omp[1] + MSVC_LINK_ARGS
				else:
					return omp[1] + DEFAULT_LINK_ARGS
			else:
				return omp[1] + extra_link_args
		
		class build_ext_with_compiler_detection(build_ext):
			def build_extensions(self):
				is_msvc = self.compiler.compiler_type=="msvc"
				
				for extension in self.extensions:
					extension.extra_link_args = determine_link_args(is_msvc)
					extension.extra_compile_args = determine_compile_args(is_msvc)
				
				build_ext.build_extensions(self)
		
		setup(
				name = self._modulename,
				ext_modules = [extension],
				script_args = script_args,
				verbose = verbose,
				cmdclass = {'build_ext':build_ext_with_compiler_detection}
			)
		
		self.jitced = find_and_load_module(self._modulename,self._tmpfile())
		self.compile_attempt = True
	
	def save_compiled(self, destination="", overwrite=False):
		"""
		saves the module file with the compiled functions for later use (see the `module_location` argument). If no compiled derivative exists, it tries to compile it first using `compile_C`. In most circumstances, you should not rename this file, as the filename is needed to determine the module name.
		
		Parameters
		----------
		destination : string specifying a path
			If this specifies only a directory (don’t forget the trailing `/` or similar), the module will be saved to that directory. If empty (default), the module will be saved to the current working directory. Otherwise, the functions will be (re)compiled to match that filename. A file ending will be appended if needed.
		overwrite : boolean
			Whether to overwrite the specified target if it already exists.
		
		Returns
		-------
		filename : string
			The destination that was actually used.
		"""
		
		folder, filename = path.split(destination)
		
		if filename:
			destination = add_suffix(destination)
			modulename = modulename_from_path(filename)
			if modulename != self._modulename:
				self.compile_C(modulename=modulename)
				self.report("compiled C code")
			else:
				self._compile_C()
			sourcefile = get_module_path(self._modulename, self._tmpfile())
		else:
			self._compile_C()
			sourcefile = get_module_path(self._modulename, self._tmpfile())
			destination = path.join(folder, add_suffix(self._modulename))
			self.report("saving file to " + destination)
		
		if not self.compile_attempt:
			raise RuntimeError("Compilation failed. Cannot save module file.")
		
		if path.isfile(destination) and not overwrite:
			raise OSError("Target File already exists and \"overwrite\" is set to False")
		else:
			shutil.copy(sourcefile, destination)
		
		return destination
	
	def __del__(self):
		try:
			shutil.rmtree(self._tmpdir)
		except (OSError, AttributeError, TypeError):
			pass

