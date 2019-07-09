'''
This is the entrypoint module for Jupyter Server Extension
'''

from .serverextension import PackageManagerHandler


def load_jupyter_server_extension(nb_server_app):
    PackageManagerHandler(nb_server_app)
