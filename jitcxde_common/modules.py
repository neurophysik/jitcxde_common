from sys import version_info

if version_info < (3,3):
	raise NotImplementedError("Python versions below 3.3 are not supported anymore (or never were). Please upgrade to a newer Python version.")
elif (3,3) <= version_info < (3,5):
	from jitcxde_common.modules_33 import get_module_path, modulename_from_path, find_and_load_module, module_from_path, add_suffix
elif (3,5) <= version_info:
	from jitcxde_common.modules_35 import get_module_path, modulename_from_path, find_and_load_module, module_from_path, add_suffix

