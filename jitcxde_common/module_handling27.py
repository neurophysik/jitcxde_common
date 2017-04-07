from __future__ import print_function, division, with_statement
from os import path
from imp import find_module, load_module, load_dynamic
from jitcxde_common.strings import remove_suffix

def modulename_from_path(full_path):
	filename = path.basename(full_path)
	return remove_suffix(filename, ".so")

def get_module_path(modulename, folder=""):
	return find_module(modulename, [folder])[1]

def find_and_load_module(modulename, folder=""):
	specs = find_module(modulename, [folder])
	return load_module(modulename, *specs)

def module_from_path(full_path):
	return load_dynamic( modulename_from_path(full_path), full_path )

