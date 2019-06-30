"""
This is the entrypoint module for Jupyter Server Extension
"""

import sys
from notebook.utils import url_path_join

from .serverextension import PackageManagerHandler


def load_jupyter_server_extension(nb_server_app):
    PackageManagerHandler(nb_server_app)
