Common Information for JiTCODE, JiTCDDE, and JiTCSDE
====================================================

The following is some detailed information on aspects common to `JiTCODE`_, `JiTCDDE`_, and `JiTCSDE`_.
As these are rather advanced topics, please read the respective documentation of the module you want to use first.

In the following, *JiTC*DE* refers to any of the aforementioned modules.

Compiler and Linker Arguments
-----------------------------

You may want to modify the default compiler and linker arguments for two reasons:

* To tweak the compilation process and results.
* To make JiTC*DE run with a compiler that doesn’t recognise the default arguments.

The default arguments are listed below and can be obtained by imports such as:

	from jitcxde_common import DEFAULT_COMPILE_ARGS

Modify these to get the most of future versions of JiTC*DE.
In either case, these arguments are appended to (and thus overwrite) whatever Setuptools uses as a default.

.. automodule:: _jitcxde
	:members:
	:exclude-members: jitcxde


.. _JiTCODE: http://github.com/neurophysik/jitcode

.. _JiTCDDE: http://github.com/neurophysik/jitcdde

.. _JiTCSDE: http://github.com/neurophysik/jitcsde

.. _SymPy Issue 4596: https://github.com/sympy/sympy/issues/4596

.. _SymPy Issue 8997: https://github.com/sympy/sympy/issues/8997

