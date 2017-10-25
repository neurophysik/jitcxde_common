// Simple template for testing purposes, consisting mainly of boilerplate.

# define NPY_NO_DEPRECATED_API NPY_1_8_API_VERSION
# include <Python.h>
# include <numpy/arrayobject.h>
# include <math.h>

# define TYPE_INDEX NPY_DOUBLE

unsigned int const dimension={{n}};

# define y(i) (* (double *) PyArray_GETPTR1(Y, i))
# define set_dy(i, value) (* (double *) PyArray_GETPTR1(dY, i) = value)

# include "f_definitions.c"

static PyObject * py_f(PyObject *self, PyObject *args)
{
	PyArrayObject * Y;
	
	if (!PyArg_ParseTuple(args,"O!",&PyArray_Type, &Y))
	{
		PyErr_SetString(PyExc_ValueError,"Wrong input.");
		return NULL;
	}
	
	if (PyArray_NDIM(Y) != 1)
	{
		PyErr_SetString(PyExc_ValueError,"Array must be one-dimensional.");
		return NULL;
	}
	else if ((PyArray_TYPE(Y) != TYPE_INDEX))
	{
		PyErr_SetString(PyExc_TypeError,"Array needs to be of type double.");
		return NULL;
	}
	
	npy_intp dims[1] = {dimension};
	PyArrayObject * dY = (PyArrayObject *) PyArray_EMPTY(1, dims, TYPE_INDEX, 0);
	
	if (dY == NULL)
	{
		PyErr_SetString (PyExc_ValueError, "Error: Could not allocate array.");
		exit(1);
	}
	
	# include "f.c"
	
	return PyArray_Return(dY);
}

static PyMethodDef {{module_name}}_methods[] = {
	{"f", py_f, METH_VARARGS, NULL},
	{NULL, NULL, 0, NULL}
};

static struct PyModuleDef moduledef =
{
	PyModuleDef_HEAD_INIT,
	"{{module_name}}",
	NULL,
	-1,
	{{module_name}}_methods,
	NULL,
	NULL,
	NULL,
	NULL
};

PyMODINIT_FUNC PyInit_{{module_name}}(void)
{
	PyObject * module = PyModule_Create(&moduledef);
	import_array();
	return module;
}

