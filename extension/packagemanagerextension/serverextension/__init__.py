"""
This is the entrypoint module for Jupyter Server Extension
"""

import sys
from notebook.utils import url_path_join

if sys.version_info >= (3, 0):
    from .serverextension import PackageManagerHandler
else:
    from serverextension import PackageManagerHandler


def load_jupyter_server_extension(nb_server_app):
    PackageManagerHandler(nb_server_app)
    print("Jupyter-Package-Manager: ServerExtension Loaded")
