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

from .envmanager import EnvManager

import projectmanagement
import packagemanagement

static = os.path.join(os.path.dirname(__file__), 'static')

NS = r'api/packagemanager'


# -----------------------------------------------------------------------------
# URL to handler mappings
# -----------------------------------------------------------------------------


default_handlers = [
    (r"/projects", projectmanagement.ManageProjectsHandler),
    (r"/project_info", projectmanagement.ProjectInfoHandler),
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
