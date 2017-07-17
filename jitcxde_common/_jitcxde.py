#!/usr/bin/python3
# -*- coding: utf-8 -*-

from __future__ import print_function

from tempfile import mkdtemp
from os import path
from inspect import stack
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import shutil
from sys import version_info, modules
from warnings import warn
from traceback import format_exc

import numpy
from jinja2 import Environment, FileSystemLoader

from .module_handling import get_module_path, modulename_from_path, find_and_load_module, module_from_path, add_suffix
from .strings import count_up

#: A list with the default extra compile arguments. Note that without `-Ofast`, `-ffast-math`, or `-funsafe-math-optimizations` (if supported by your compiler), you may experience a considerable speed loss since SymPy uses the `pow` function for small integer powers (`SymPy Issue 8997`_). 
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

#: A list with the default compile arguments for the Microsoft compiler. I could not find what level of optimisation is needed to address the problem of SymPy using the `pow` function for small integer powers (`SymPy Issue 8997`_).
MSVC_COMPILE_ARGS = [
			"/Ox",
			"/wd4068",
			"/wd4146",
			"/wd4018"
			]

#: A list with the default linker arguments for the Microsoft compiler.
MSVC_LINK_ARGS = [ "/ignore:4197" ]

class build_ext_with_compiler_detection(build_ext):
	def build_extensions(self):
		for extension in self.extensions:
			if self.compiler.compiler_type=="msvc":
				extension.extra_compile_args = MSVC_COMPILE_ARGS
				extension.extra_link_args    = MSVC_LINK_ARGS
			else:
				extension.extra_compile_args = DEFAULT_COMPILE_ARGS
				extension.extra_link_args    = DEFAULT_LINK_ARGS
		
		build_ext.build_extensions(self)

class jitcxde(object):
	"""
	A base class containing elementary, common functionalities of all JiTC*DE projects – mostly file handling. It is pretty dysfunctional on its own and only made to be inherited from.
	"""
	
	def __init__(self,verbose,module_location):
		self._tmpdir = None
		self.verbose = verbose
		self._modulename = "jitced"
		
		if module_location is not None:
			self.jitced = module_from_path(module_location)
			self.compile_attempt = True
		else:
			self.jitced = None
			self.compile_attempt = None
		
	
	def _tmpfile(self,filename=None):
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
		kwargs["module_name"] = self._modulename
		kwargs["Python_version"] = version_info[0]
		folder = path.dirname( stack()[1][1] )
		env = Environment(loader=FileSystemLoader(folder))
		template = env.get_template("jitced_template.c")
		with open(self.sourcefile, "w") as codefile:
			codefile.write(template.render(kwargs))
	
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
	
	def _compile_and_load(self,verbose,extra_compile_args,extra_link_args=None):
		auto_args = extra_link_args is None and extra_compile_args is None
		
		extension = Extension(
				self._modulename,
				sources = [self.sourcefile],
				extra_link_args = extra_link_args,
				include_dirs = [numpy.get_include()],
				extra_compile_args = extra_compile_args,
				)
		
		script_args = [
				"build_ext",
				"--build-lib", self._tmpfile(),
				"--build-temp", self._tmpfile(),
				"--force",
				#"clean" #, "--all"
				]
		
		setup(
			name = self._modulename,
			ext_modules = [extension],
			script_args = script_args,
			verbose = verbose,
			cmdclass = {'build_ext':build_ext_with_compiler_detection} if auto_args else {}
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

