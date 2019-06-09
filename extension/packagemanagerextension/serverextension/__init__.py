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
    web_app = nb_server_app.web_app
    host_pattern = '.*$'

    # handler for API.
    web_app.add_handlers(host_pattern, [
        (url_path_join(web_app.settings['base_url'], r'/api/packagemanager'),
         PackageManagerHandler)
    ])
    print("JupyterPackageManager: ServerExtension Loaded")
