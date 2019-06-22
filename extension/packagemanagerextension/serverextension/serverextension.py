# pylint: disable=W0221

# Tornado get and post handlers often have different args from their base class
# methods.

import json
import os
import re
import sys

from subprocess import Popen
from tempfile import TemporaryFile

from pkg_resources import parse_version
from notebook.utils import url_path_join as ujoin
from notebook.base.handlers import (
    APIHandler,
    json_errors,
)
from tornado import web, escape

if sys.version_info >= (3, 0):
    from .envmanager import EnvManager, package_map
else:
    from envmanager import EnvManager, package_map

import projectmanagement
import packagemanagement

static = os.path.join(os.path.dirname(__file__), 'static')

NS = r'api/packagemanager'


# -----------------------------------------------------------------------------
# URL to handler mappings
# -----------------------------------------------------------------------------


# there is almost no text that is invalid, but no hyphens up front, please
# neither all these suspicious but valid caracthers...
_env_regex = r"(?P<env>[^/&+$?@<>%*-][^/&+$?@<>%*]*)"

# no hyphens up front, please
_pkg_regex = r"(?P<pkg>[^\-][\-\da-zA-Z\._]+)"


default_handlers = [
    (r"/projects", projectmanagement.ManageProjectsHandler),
    (r"/environments/%s" % _env_regex, projectmanagement.ExportEnvHandler),
    (r"/environment_clone", projectmanagement.CloneEnvHandler),
    (r"/packages", packagemanagement.PkgHandler),
    (r"/packages/check_update", packagemanagement.CheckUpdatePkgHandler),
    (r"/packages/available", packagemanagement.AvailablePackagesHandler),
    (r"/packages/search", packagemanagement.SearchHandler),
]


def PackageManagerHandler(nbapp):
    """Load the nbserver extension"""
    webapp = nbapp.web_app
    webapp.settings['env_manager'] = EnvManager(parent=nbapp)

    base_url = webapp.settings['base_url']
    webapp.add_handlers(".*$", [
        (ujoin(base_url, NS, pat), handler)
        for pat, handler in default_handlers
    ])
    nbapp.log.info("packagemanagerextension: Handlers enabled")
