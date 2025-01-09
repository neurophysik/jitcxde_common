from importlib.machinery import EXTENSION_SUFFIXES, ExtensionFileLoader, FileFinder
from importlib.util import module_from_spec, spec_from_file_location
from os import path


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
	module = module_from_spec(spec)
	spec.loader.exec_module(module)
	return module

def module_from_path(full_path):
	modulename = modulename_from_path(full_path)
	spec = spec_from_file_location(modulename, full_path)
	module = module_from_spec(spec)
	spec.loader.exec_module(module)
	return module

