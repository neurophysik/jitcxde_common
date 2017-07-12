from __future__ import print_function, division, with_statement
from os import path
from importlib.machinery import ExtensionFileLoader, EXTENSION_SUFFIXES, FileFinder
from importlib.util import spec_from_file_location

loader_details = (ExtensionFileLoader, EXTENSION_SUFFIXES)
suffices = sorted(EXTENSION_SUFFIXES, key=len)

def remove_suffix(path):
	for suffix in reversed(suffices):
		if path.endswith(suffix):
			return path.rpartition(suffix)[0]
	else:
		return path

def add_suffix(path):
	for suffix in suffices:
		if path.endswith(suffix):
			return path
	else:
		return path + suffices[0]

def modulename_from_path(full_path):
	return remove_suffix(path.basename(full_path))

def get_module_path(modulename, folder=""):
	finder = FileFinder(folder, loader_details)
	return finder.find_spec(modulename).origin

def find_and_load_module(modulename, folder=""):
	finder = FileFinder(folder, loader_details)
	spec = finder.find_spec(modulename)
	return spec.loader.load_module()

def module_from_path(full_path):
	modulename = modulename_from_path(full_path)
	spec = spec_from_file_location(modulename, full_path)
	return spec.loader.load_module()

