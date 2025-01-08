from sys import version_info


if version_info < (3,3):  # noqa: UP036
	raise NotImplementedError("Python versions below 3.3 are not supported anymore (or never were). Please upgrade to a newer Python version.")
elif (3,3) <= version_info < (3,5):
	from jitcxde_common.modules_33 import add_suffix, find_and_load_module, get_module_path, module_from_path, modulename_from_path
elif (3,5) <= version_info:
	from jitcxde_common.modules_35 import add_suffix, find_and_load_module, get_module_path, module_from_path, modulename_from_path  # noqa: F401

