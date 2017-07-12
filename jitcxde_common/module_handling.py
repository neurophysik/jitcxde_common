from sys import version_info

if version_info < (3,):
	from .module_handling27 import get_module_path, modulename_from_path, find_and_load_module, module_from_path, add_suffix
elif (3,) <= version_info < (3,3):
	raise NotImplementedError("Module loading for Python versions between 3 and 3.3 was not implemented. Please upgrade to a newer Python version.")
elif (3,3) <= version_info < (3,5):
	from .module_handling33 import get_module_path, modulename_from_path, find_and_load_module, module_from_path, add_suffix
elif (3,5) <= version_info:
	from .module_handling35 import get_module_path, modulename_from_path, find_and_load_module, module_from_path, add_suffix

