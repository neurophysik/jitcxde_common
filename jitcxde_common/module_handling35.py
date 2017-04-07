from __future__ import print_function, division, with_statement
from os import path
from importlib.util import module_from_spec
from importlib.machinery import ExtensionFileLoader, EXTENSION_SUFFIXES, FileFinder
from importlib.util import spec_from_file_location
from jitcxde_common.strings import remove_suffix

loader_details = (ExtensionFileLoader, EXTENSION_SUFFIXES)

def modulename_from_path(full_path):
	filename = path.basename(full_path)
	for suffix in sorted(EXTENSION_SUFFIXES, key=len, reverse=True):
		filename = remove_suffix(filename, suffix)
	return filename

def get_module_path(modulename, folder=""):
	finder = FileFinder(folder, loader_details)
	return finder.find_spec(modulename).origin

def find_and_load_module(modulename, folder=""):
	finder = FileFinder(folder, loader_details)
	spec = finder.find_spec(modulename)
	module = module_from_spec(spec)
	spec.loader.exec_module(module)
	return module

def module_from_path(full_path):
	modulename = modulename_from_path(full_path)
	spec = spec_from_file_location(modulename, full_path)
	module = module_from_spec(spec)
	spec.loader.exec_module(module)
	return module

