#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import platform
import shutil
from tempfile import mkdtemp
import unittest

import sympy
import numpy

from jitcxde_common import jitcxde,handle_input,render_and_write_code

y = sympy.Function("y")
f = [
		y(0),
		2*y(1)**3,
		y(0)+y(1)+y(2),
		sympy.exp(y(3)),
		5,
	]

def f_control(y):
	return [
		y[0],
		2*y[1]**3,
		y[0]+y[1]+y[2],
		numpy.exp(y[3]),
		5,
	]

def f_generator():
	for entry in f:
		yield entry


class jitcxde_tester(jitcxde):
	def __init__(self,f_sym=(),n=None,module_location=None,chunk_size=100):
		jitcxde.__init__(self,False,module_location)
		f_sym_wc,self.n = handle_input(f_sym,n)
		set_dy = sympy.Function("set_dy")
		
		render_and_write_code(
			(set_dy(i,entry) for i,entry in enumerate(f_sym_wc())),
			tmpfile = self._tmpfile,
			name = "f",
			functions = ["set_dy", "y"],
			chunk_size = chunk_size,
			arguments = [
					("Y" , "PyArrayObject *__restrict const"),
					("dY", "PyArrayObject *__restrict const")
				]
			)
	
	def _compile_C(self):
		if self.jitced is None:
			self.compile_C()
	
	def compile_C(self,modulename=None):
		self._process_modulename(modulename)
		self._render_template(n=self.n)
		self._compile_and_load(False,None,None)


name = ""
def get_unique_name():
	global name
	name += "x"
	return name

class basic_test(unittest.TestCase):
	def tmpfile(self, filename):
		return os.path.join(self.directory, filename)
	
	@classmethod
	def setUpClass(self):
		self.argdict = {"f_sym": f}
	
	def setUp(self):
		self.directory = mkdtemp()
		self.tester = jitcxde_tester(**self.argdict)
	
	def test_default(self):
		self.tester.compile_C()
	
	def test_save_and_load(self):
		destination = self.tester.save_compiled(overwrite=True)
		folder, filename = os.path.split(destination)
		shutil.move(filename,self.tmpfile(filename))
		self.tester = jitcxde_tester(module_location=self.tmpfile(filename))
		
	def test_compile_save_and_load(self,default=False):
		modulename = None if default else get_unique_name()
		self.tester.compile_C(modulename=modulename)
		filename = self.tester.save_compiled(overwrite=True)
		shutil.move(filename, self.tmpfile(filename))
		self.tester = jitcxde_tester(module_location=self.tmpfile(filename))
		
	def test_save_with_default_name_and_load(self):
		self.test_compile_save_and_load(True)
	
	def test_save_to_directory_and_load(self):
		modulename = get_unique_name()
		self.tester.compile_C(modulename=modulename)
		destination = self.tester.save_compiled(self.tmpfile(""), overwrite=True)
		folder, filename = os.path.split(destination)
		print(folder,self.tmpfile(""))
		assert folder==os.path.dirname(self.tmpfile(""))
		self.tester = jitcxde_tester(module_location=self.tmpfile(filename))
	
	def tearDown(self):
		arg = numpy.random.uniform(-2,2,5)
		numpy.testing.assert_allclose(
				self.tester.jitced.f(arg),
				f_control(arg)
			)
		
		if platform.system() != "Windows":
			# Windows blocks loaded module files from removal.
			shutil.rmtree(self.directory)

class basic_test_with_chunking(basic_test):
	@classmethod
	def setUpClass(self):
		self.argdict = {"f_sym":f, "chunk_size":1}

class basic_test_with_generator_function(basic_test):
	@classmethod
	def setUpClass(self):
		self.argdict = {"f_sym":f_generator, "n":len(f)}

if __name__ == "__main__":
	unittest.main(buffer=True)

