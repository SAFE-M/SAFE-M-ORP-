project = 'SAFE-M-ORP'
copyright = '2026, Mathis Velasco'
author = 'Mathis Velasco, François Métivier'
release = '1'

import os
import sys
sys.path.insert(0, os.path.abspath('../SRC'))  # pour autodoc, doit pointer vers ton code

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.coverage', 'sphinx.ext.napoleon']
templates_path = ['_templates']
exclude_patterns = []
language = 'fr'

html_theme = 'furo'
html_static_path = ['_static']

# --- Configuration spécifique à la sortie PDF (LaTeX) ---
latex_docclass = {
    'manual': 'ipgpsphinxmanual',   # ← ta nouvelle classe
}
latex_elements = {
    'papersize': 'a4paper',
    'pointsize': '11pt',
}
latex_additional_files = ['ipgpsphinxmanual.cls']  # ← indispensable !
latex_logo = 'images/logo_ipgp.png'  # optionnel, si tu as le logo en image