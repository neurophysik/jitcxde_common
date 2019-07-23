import sys
import os
from unittest.mock import MagicMock as Mock
from setuptools_scm import get_version

# Mocking to make RTD autobuild the documentation. (Doesn’t suffice.)
# autodoc_mock_imports = [ 'numpy', 'symengine', '.' ]

MOCK_MODULES = [
	'numpy', 'numpy.testing', 'numpy.random',
	'symengine', 'symengine.printing', 'symengine.lib.symengine_wrapper',
	'.'
]
sys.modules.update((mod_name, Mock()) for mod_name in MOCK_MODULES)

sys.path.insert(0,os.path.abspath("../jitcxde_common"))

needs_sphinx = '1.3'

extensions = [
		'sphinx.ext.autodoc',
		'sphinx.ext.autosummary',
		'sphinx.ext.mathjax',
		'numpydoc',
	]

source_suffix = '.rst'

master_doc = 'index'

project = u'JiTC*DE Common'
copyright = u'2017, Gerrit Ansmann'

release = version = get_version(root='..', relative_to=__file__)

default_role = "any"

add_function_parentheses = True

add_module_names = False

html_theme = 'nature'
pygments_style = 'colorful'
htmlhelp_basename = 'JiTC*DEdoc'

numpydoc_show_class_members = False
autodoc_member_order = 'bysource'

def on_missing_reference(app, env, node, contnode):
	if node['reftype'] == 'any':
		return contnode
	else:
		return None

def setup(app):
	app.connect('missing-reference', on_missing_reference)
