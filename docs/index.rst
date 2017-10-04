Common Information for JiTCODE, JiTCDDE, and JiTCSDE
====================================================

The following is some detailed information on aspects common to `JiTCODE`_, `JiTCDDE`_, and `JiTCSDE`_.
As these are rather advanced topics, please read the respective documentation of the module you want to use first.

In the following, *JiTC*DE* refers to any of the aforementioned modules.

Installation
------------

Linux (and other Unixes, like MacOS)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*	Usually, you will already have a C compiler installed and need not worry about this step.
	Otherwise, it should be easy to install GCC or Clang through your package manager.
	Note that for using Clang, it may be necessary to change the `CC` flag (see below).

*	Python should be installed by default as well.

*	The easiest way to install JiTC*DE is via PyPi like this:
	
	.. code-block:: bash
	
		pip3 install jitcode --user
	
	Replace `jitcode` with `jitcdde` or `jitcsde` if that’s what you want.
	Replace `pip3` with `pip` if you are working in an environment or with Python 2.

Windows (Anaconda)
^^^^^^^^^^^^^^^^^^

*	Install Anaconda.

*	Install a C compiler.
	The only one that Setuptools uses without a major struggle is from `Microsoft Build Tools for Visual Studio <http://landinghub.visualstudio.com/visual-cpp-build-tools>`_
	For more details and everything else, see `this site <https://wiki.python.org/moin/WindowsCompilers>`_.

*	Open the Anaconda Prompt and run:
	
	.. code-block:: bash
	
		pip install jitcode --user
	
	Replace `jitcode` with `jitcdde` or `jitcsde` if that’s what you want.

Networks or other very large differential equations
---------------------------------------------------

JiTC*DE is specifically designed to be able to handle large differential equations, as they arise, e.g., in networks.
There is an explicit `example of a network`_ in JiTCODE’s documentation, which is straightforward to translate to JiTCDDE and JiTCSDE.

For very large differential equations, there are two sources of memory or speed problems:

*	**The compiler**,
	who has to compile megabytes of unstructured code and tries to handle it all at once, which may use too much time and memory. For some compilers, disabling all optimisation can avert this problem, but then, compiler optimisations usually are a good thing.
	
	As a compromise, JiTC*DE structures large source code into chunks, which the compiler then handles separately. This way optimisation can happen within the chunks, but not across chunks. The precise size of those chunks can be controlled by the option `chunk_size` which is available for all code-generation subroutines.
	If there is an obvious grouping of your :math:`f`, the group size suggests itself for `chunk_size`.
	For example, if you want to simulate the dynamics of three-dimensional oscillators coupled onto a 40×40 lattice and if the differential equations are grouped first by oscillator and then by lattice row, a chunk size of 120 suggests itself.
	
	We obtained better performances in these regards with Clang than with GCC.
	

*	**SymPy’s cache**,
	which may use too much memory. While it can be completely deactivated by setting the environment variable `SYMPY_USE_CACHE=no`, it exists for a reason and may speed things up.
	
	To address this, JiTC*DE clears the cache after each chunk is written and accepts generator functions as an input for :math:`f` (or similar), which makes SymPy’s handling of an entry happen right before the corresponding code is generated.
	See the `example of a network`_ from JiTCODE’s documentation for an example how to use a generator function.

Also note that simplifications and common-subexpression eliminations may take a considerable amount of time (and can be disabled).
In particular, if you want to calculate the Lyapunov exponents of a larger system, it may be worthwhile to set `simplify` to `False`.

Choosing the Compiler
---------------------

Linux (and other Unixes, like MacOS)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Setuptools uses your operating system’s `CC` flag to choose the compiler.
Therefore, this is what you have to change, if you want to change the compiler.
Some common ways to do this are (using `clang` as an example for the desired compiler):

* Call `export CC=clang` in the terminal before running JiTC*DE. Note that you have to do this anew for every instance of the terminal or write it into some configuration file.
* Call `os.environ["CC"] = "clang"` in Python.

So far, Clang has proven to be better at handling large differential equations.

Windows
^^^^^^^

I haven’t tried it myself, but `this site <https://wiki.python.org/moin/WindowsCompilers>`_ should help you.

Choosing the Module Name
------------------------

The only reason why you may want to change the module name is if you want to save the module file for later use (with `save_compiled`).
To do this use the `modulename` argument of the `compile_C` command.
If this argument is `None` or empty, the filename will be chosen by JiTC*DE based on previously used filenames or default to `jitced.so`.

Note that it is not possible to re-use a modulename for a given instance of Python (due to the limitations of Python’s import machinery).

Compiler and Linker Arguments
-----------------------------

All classes have a `compile_C` command which has `extra_compile_args` and `extra_link_args` as an argument.
If those arguments are left `None`, defaults (listed below) are chosen depending on the compiler that Setuptools actually uses.
You may want to modify the these arguments for two reasons:

* To tweak the compilation process and results.
* To make JiTC*DE run with a compiler that doesn’t recognise the default arguments.

In most situation, it’s best not to write your own list, but modify the defaults listed below.
These can be imported from `jitcxde_common` like this:

.. code-block:: python

	from jitcxde_common import DEFAULT_COMPILE_ARGS

You can then modify them before usage, e.g., like this:

. code-block:: python

	ODE.compile_C(extra_compile_args = DEFAULT_COMPILE_ARGS + ["--my-flag"])

This way you get the most of future versions of JiTC*DE.

Note that in either case, these arguments are appended to (and thus override) whatever Setuptools uses as a default.

.. automodule:: _jitcxde
	:members:
	:exclude-members: jitcxde

.. _large_systems:

Common Mistakes
---------------

*	If you want to use mathematical functions like `sin`, `exp` or `sqrt` you have to use the SymPy variants.
	For example, instead of `math.sin` or `numpy.sin`, you have to use `sympy.sin`.

*	If JiTC*DE is too slow, check whether you deactivated simplifications and common-subexpression eliminations, used a generator and avoided `SymPy Issue 4596`_.

.. _JiTCODE: https://github.com/neurophysik/jitcode

.. _JiTCDDE: https://github.com/neurophysik/jitcdde

.. _JiTCSDE: https://github.com/neurophysik/jitcsde

.. _SymPy Issue 4596: https://github.com/sympy/sympy/issues/4596

.. _SymPy Issue 8997: https://github.com/sympy/sympy/issues/8997

.. _example of a network: https://jitcode.readthedocs.io/#module-SW_of_Roesslers
