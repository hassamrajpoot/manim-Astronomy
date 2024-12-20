import os
import sys
sys.path.insert(0, os.path.abspath('../..')) 
sys.path.insert(0, os.path.abspath('.')) 

project = 'Astronomy Plugin for Manim'
author = 'Hassam ul Haq'
release = '0.0.3'


extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.autosummary',
    'sphinxcontrib.video' 
]


master_doc = 'index'
