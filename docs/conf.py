import os
import sys
sys.path.insert(0, os.path.abspath('../..'))  # Adjust path if needed

project = 'Astronomy Plugin for Manim'
author = 'Hassam ul Haq'
release = '0.0.1'


extensions = [
    'sphinx.ext.autodoc',  
    'sphinx.ext.napoleon',  
]


master_doc = 'index'
