from __future__ import print_function, division, with_statement
from os import path
from imp import find_module, load_module, load_dynamic, get_suffixes

raw_suffices = [S[0] for S in get_suffixes() if S[2]==3 and S[0][0]=="."]
suffices = sorted(raw_suffices, key=len)

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
	filename = path.basename(full_path)
	return remove_suffix(filename)

def get_module_path(modulename, folder=""):
	return find_module(modulename, [folder])[1]

def find_and_load_module(modulename, folder=""):
	specs = find_module(modulename, [folder])
	return load_module(modulename, *specs)

def module_from_path(full_path):
	return load_dynamic( modulename_from_path(full_path), full_path )

