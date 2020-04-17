Common Information for JiTCODE, JiTCDDE, and JiTCSDE
====================================================

The following is some detailed information on aspects common to `JiTCODE`_, `JiTCDDE`_, and `JiTCSDE`_.

In the following, *JiTC*DE* refers to any of the aforementioned modules.

Installation
------------

Unix (Linux, MacOS, …)
^^^^^^^^^^^^^^^^^^^^^^

*	Usually, you will already have a C compiler installed and need not worry about this step.
	Otherwise, it should be easy to install GCC or Clang through your package manager.
	Note that for using Clang, it may be necessary to change the `CC` flag (see below).
	Finally note that getting OpenMP support (see below) for Clang on MacOS `seems to be a hassle <https://stackoverflow.com/q/43555410/2127008>`_.

*	Python should be installed by default as well.

*	The easiest way to install JiTC*DE is via PyPi like this:
	
	.. code-block:: bash
	
		pip3 install jitcode --user
	
	Replace `jitcode` with `jitcdde` or `jitcsde` if that’s what you want.
	Replace `pip3` with `pip` if you are working in an environment.

Windows (Anaconda)
^^^^^^^^^^^^^^^^^^

*	Install Anaconda.

*	Install a C compiler.
	The only one that Setuptools uses without a major struggle is from `Microsoft Build Tools for Visual Studio <https://docs.microsoft.com/visualstudio/install>`_
	For more details and everything else, see `this site <https://wiki.python.org/moin/WindowsCompilers>`_.

*	Open the Anaconda Prompt and run:
	
	.. code-block:: bash
	
		pip install jitcode --user
	
	Replace `jitcode` with `jitcdde` or `jitcsde` if that’s what you want.

Building from source
^^^^^^^^^^^^^^^^^^^^
Usually you do not need to do this, but it may be the only way if prepackaged SymEngine doesn’t work on your system.

*	Install SymEngine from source following the instructions `here <https://github.com/symengine/symengine#building-from-source>`_.

*	Install the SymEngine Python bindings from source following the instructions `here <https://github.com/symengine/symengine.py#build-from-source>`_.

*	Install readily available required Python packages, namely Jinja 2, NumPy, SciPy, and Setuptools.

*	Install JiTC*DE Common and the desired packages from GitHub.
	The easiest way to do this is probably:
	
	.. code-block:: bash
	
		pip3 install git+git://github.com/neurophysik/jitcode
	
	Replace `jitcode` with `jitcxde_common`, `jitcdde`, or `jitcsde` accordingly.

Here is a summary of commands for Ubuntu (that should be easily adaptable to most other Unixes):

.. code-block:: bash

	sudo apt install cmake cython git libgmp-dev python3-jinja2 python3-numpy python3-scipy python3-setuptools
	
	git clone https://github.com/symengine/symengine
	cd symengine
	cmake .
	make
	sudo make install
	
	pip3 install \
		git+git://github.com/symengine/symengine.py \
		git+git://github.com/neurophysik/jitcxde_common \
		git+git://github.com/neurophysik/jitcode \
		git+git://github.com/neurophysik/jitcdde \
		git+git://github.com/neurophysik/jitcsde \
		--no-dependencies --user

Testing the Installation
^^^^^^^^^^^^^^^^^^^^^^^^
Each module provides a utility function that runs a short basic test of the installation, in particular whether a compiler is present and can be interfaced. For example, you can call it as follows:

.. code-block:: python

	import jitcode
	jitcode.test()

.. _large_systems:

Networks or other very large differential equations
---------------------------------------------------

JiTC*DE is specifically designed to be able to handle large differential equations, as they arise, e.g., in networks.
There is an explicit `example of a network`_ in JiTCODE’s documentation, which is straightforward to translate to JiTCDDE and JiTCSDE.

Chunking
^^^^^^^^

JiTC*DE structures large source code into chunks, the size of which can be controlled by the option `chunk_size`, which is available for all code-generation subroutines.
This has two reasons or uses:

*	If JiTC*DE handled the code for very large differential equations naïvely, a problem would arise from the compiler trying to handle megabytes of unstructured code at once, which may use too much time and memory.
	For some compilers, disabling all optimisation can avert this problem, but then, compiler optimisations usually are a good thing.
	Chunking is a compromise between the two:
	Optimisation still happens within chunks, but not across chunks.
	We obtained better performances in these regards with Clang than with GCC.

*   It allows a reasonable parallelisation using OpenMP (see the next section). Note that `chunk_size` here is also used for regular loops and similar.

If there is an obvious grouping of your :math:`f`, the group size suggests itself for `chunk_size`.
For example, if you want to simulate the dynamics of three-dimensional oscillators coupled onto a 40×40 lattice and if the differential equations are grouped first by oscillator and then by lattice row, a chunk size of 120 suggests itself.

Also note that simplifications and common-subexpression eliminations may take a considerable amount of time (and can be disabled).
In particular, if you want to calculate the Lyapunov exponents of a larger system, it may be worthwhile to set `simplify` to `False`.

OpenMP Support (multi-processing)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Code generated by JiTCODE contains OpenMP pragmas that will make the compiler automatically compile the code such that it will be parallelised on a multi-kernel machine – if the right respective compiler and linker flags are used and the respective libraries are installed.
Each compiling command has an argument `omp` that when set to `True` will cause the most generic of these flags to be used.
Depending on the compiler, these flags may not work or not be the best choice.
In this case you pass the desired compiler and linker flags as a pair of lists of strings to the `omp` argument.
For example, for GCC, you might use:

	.. code-block:: bash
	
		ODE.compile_C( omp=(["-fopenmp"],["-lgomp"]) )

In most cases, the chunk sizes used by OpenMP correspond to the chunk_size argument of the respective code-generating instruction.

Note that parallelisation comes with a considerable overhead.
It is therefore **only worthwhile if both**:

*	Your differential equation is huge (ballpark: hundreds of instructions).

*	You have fewer problems (realisations) than cores or cannot run several problems in parallel due to memory constraints or similar.

Choosing the Compiler
---------------------

You can find out which compiler is used by explicitly calling `I.compile_C(verbose=True)`, where `I` is your JiTC*DE object.

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
To do this, use the `modulename` argument of the `compile_C` command.
If this argument is `None` or empty, the filename will be chosen by JiTC*DE based on previously used filenames or default to `jitced.so`.

Note that it is not possible to re-use a module name for a given instance of Python (due to the limitations of Python’s import machinery).

Compiler and Linker Arguments
-----------------------------

All classes have a `compile_C` command which has `extra_compile_args` and `extra_link_args` as an argument.
If those arguments are left `None`, defaults (listed below) are chosen depending on the compiler that Setuptools actually uses.
You may want to modify the these arguments for two reasons:

* To tweak the compilation process and results.
* To make JiTC*DE run with a compiler that doesn’t recognise the default arguments.

Often, it’s best not to write your own list, but modify the defaults listed below.
These can be imported from `jitcxde_common` like this:

.. code-block:: python

	from jitcxde_common import DEFAULT_COMPILE_ARGS

You can then modify them before usage, e.g., like this:

.. code-block:: python

	ODE.compile_C( extra_compile_args = DEFAULT_COMPILE_ARGS + ["--my-flag"] )

This way you get the most of future versions of JiTC*DE.

Note that in either case, these arguments are appended to (and thus override) whatever Setuptools uses as a default.

.. automodule:: _jitcxde
	:members:
	:exclude-members: jitcxde

SymPy vs SymEngine
------------------

`SymPy`_’s core is completely written in Python and hence rather slow.
Eventually, this core shall be replaced by a faster, compiled one: `SymEngine`_, more specifically the SymEngine Python wrapper.
SymEngine is not yet ready for this, but it already has everything needed for JiTC*DE’s purpose, except for some side features like common-subexpression elimination and lambdification (only for JiCDDE).
Also SymEngine internally resorts to SymPy for some features like simplification.
By using SymEngine instead of SymPy, code generation in JiTC*DE is up to nine hundred times faster.

Practically, you can use both SymPy and SymEngine to provide the input to JiTC*DE, as they are compatible with each other.
However, using SymPy may considerably slow down code generation.
Also, some advanced features of SymPy may not translate to SymEngine, but so far the only one I can see making sense in a typical JiTC*DE application are SymPy’s sums and those can be easily replaced by Python sums.
If you want to precprocess JiTC*DE’s input in some way that only SymPy can handle, the `sympy_symbols` submodule provides SymPy symbols that work the same as what `jitc*de` provides directly, except for speed.
Here is an example for imports that make use of this:

	.. code-block:: Python
	
		from jitcode import jitcode
		from jitcode.sympy_symbols import t,y

Note that while SymEngine’s Python wrapper is sparsely documented, almost everything that is relevant to JiTC*DE behaves analogously to SymPy and the latter’s documentation serves as a documentation for SymEngine as well.
For this reason, JiTC*DE’s documentation also often links to SymPy’s documentation when talking about SymEngine features.

Conditionals
------------

Many dynamics contain a step function, Heaviside function, conditional, or whatever you like to call it.
In the vast majority of cases you cannot naïvely implement this, because discontinuities can lead to all sorts of problems with the integrators.
Most importantly, error estimation and step-size adaption requires a continuous derivative.
Moreover, any Python conditionals will be evaluated during the code generation and not at runtime, which not what you want in this case.

There are two general ways to solve this:

*	If your step-wise behaviour depends on time (e.g., an external pulse that is limited in time), integrate up to the point of the step, change `f` or a control parameter, and continue.
	Note that for DDEs this may introduce a discontinuity that needs to be dealt with like an initial discontinuity.

*	Use a sharp sigmoid instead of the step function.
	`jitcxde_common` provides a service function `conditional` which can be used for this purpose and is documented below.

.. autofunction:: symbolic.conditional

Common Mistakes and Questions
-----------------------------

*	If you want to use mathematical functions like `sin`, `exp` or `sqrt` you have to use the SymEngine variants.
	For example, instead of `math.sin` or `numpy.sin`, you have to use `symengine.sin`.

*	If you get unexpected or cryptic errors, please run the respective class’s `check` function and also check that all input has the right format and functions have the right signature.

*	If JiTC*DE’s code generation and compilation is too slow or bursts your memory, check:
	
	* Did you deactivate simplifications and common-subexpression eliminations?
	* Did you use a generator?
	* Did you use chunking?
	* Does disabling simplification or common-subexpression elimination (for all applicable processing steps) help?
	* Did you use SymEngine symbols and functions instead of SymPy ones?
	* Consider using Clang as a compiler.

*	There is a remote chance that you see get a `ValueError`: “assignment destination is read-only” when working with arrays returned from JiTC*DE.
	This is because the respective array directly accesses JiTC*DE’s internal state for efficiency and if you could write to this, bizarre errors would ensue.
	If you want to modify such an array, you must make a copy of it first.

.. _JiTCODE: https://github.com/neurophysik/jitcode

.. _JiTCDDE: https://github.com/neurophysik/jitcdde

.. _JiTCSDE: https://github.com/neurophysik/jitcsde

.. _SymPy Issue 8997: https://github.com/sympy/sympy/issues/8997

.. _example of a network: https://jitcode.readthedocs.io/#module-SW_of_Roesslers

.. _SymEngine: https://github.com/symengine/symengine

.. _SymPy: http://www.sympy.org/

