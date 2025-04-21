# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import os
import sys
sys.path.insert ( 0, os.path.abspath ( '../..' ) )

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'QRMaster'
copyright = '2025, Filiberto Zaá Avila'
author = 'Filiberto Zaá Avila'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration


extensions = [
  'sphinx.ext.autodoc',
  'sphinx.ext.napoleon',
  'myst_parser'
]

templates_path = [ '_templates' ]
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = [ '_static' ]

source_suffix = {
  '.rst' : 'restructuredtext',
  '.md' : 'markdown',
}

# Idioma por defecto
language = 'en'

# Idiomas adicionales (esto es más para referencia interna)
locale_dirs = [ 'locale/' ]   # ruta donde se guardarán los archivos .po
gettext_compact = False     # opcional, para mantener estructura de carpetas por archivo
