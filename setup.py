from setuptools import setup
from io import open

requirements = [
	'symengine>=0.3.1.dev0',
	'numpy',
	'jinja2',
	'setuptools'
]

setup(
	name = 'jitcxde_common',
	description = 'Common code for JiTC*DE',
	long_description = open('README.rst', encoding='utf8').read(),
	author = 'Gerrit Ansmann',
	author_email = 'gansmann@uni-bonn.de',
	url = 'http://github.com/neurophysik/jitcxde_common',
	packages = ['jitcxde_common'],
	python_requires=">=3.3",
	install_requires = requirements,
	setup_requires = ['setuptools_scm'],
	use_scm_version = {'write_to': 'jitcxde_common/version.py'},
	classifiers = [
		'Development Status :: 4 - Beta',
		'License :: OSI Approved :: BSD License',
		'Operating System :: POSIX',
		'Operating System :: MacOS :: MacOS X',
		'Operating System :: Microsoft :: Windows',
		'Programming Language :: Python',
		'Topic :: Scientific/Engineering :: Mathematics',
		],
)

