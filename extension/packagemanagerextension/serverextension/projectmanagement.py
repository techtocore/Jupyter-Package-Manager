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


class EnvBaseHandler(APIHandler):
    """
    Mixin for an env manager. Just maintains a reference to the
    'env_manager' which implements all of the conda functions.
    """
    @property
    def env_manager(self):
        """Return our env_manager instance"""
        return self.settings['env_manager']

# -----------------------------------------------------------------------------
# Project Management APIs
# -----------------------------------------------------------------------------


class ManageProjectsHandler(EnvBaseHandler):

    """
    Handler for `GET /projects` which lists the projects.
    """

    @json_errors
    def get(self):
        self.finish(json.dumps(self.env_manager.list_envs()))

    """
    Handler for `POST /projects` which
    creates the specified environment.
    """

    @json_errors
    def post(self):
        data = escape.json_decode(self.request.body)
        directory = data.get('dir') + '/'
        env_type = data.get('env_type', 'python3')
        if env_type not in package_map:
            raise web.HTTPError(400)
        resp = self.env_manager.create_project(directory, env_type)
        if 'error' not in resp:
            status = 201  # CREATED

        # catch-all ok
        if 'error' in resp:
            status = 400

        self.set_status(status or 200)
        self.finish(json.dumps(resp))

    """
    Handler for `DELETE /projects` which
    deletes the specified projects.
    """

    @json_errors
    def delete(self):
        data = escape.json_decode(self.request.body)
        directory = data.get('dir') + '/'
        resp = self.env_manager.delete_project(directory)
        if 'error' not in resp:
            status = 200

        # catch-all ok
        if 'error' in resp:
            status = 400

        self.set_status(status or 200)
        self.finish(json.dumps(resp))


class ExportEnvHandler(EnvBaseHandler):

    """
    Handler for `GET /environments/<name>` which
    exports the specified environment as a text file or simply lists all
    the packages in the specified environment, based on the Content-Type header. 
    """

    @json_errors
    def get(self, env):

        if self.request.headers.get('Content-Type') == 'application/json':
            # send list of all packages
            self.finish(json.dumps(self.env_manager.env_packages(env)))
        else:
            # export requirements file
            self.set_header('Content-Disposition',
                            'attachment; filename="%s"' % (env + '.txt'))
            self.finish(self.env_manager.export_env(env))


class CloneEnvHandler(EnvBaseHandler):

    """
    Handler for `POST /environment_clone` which
    clones the specified environment.
    """

    @json_errors
    def post(self):
        data = escape.json_decode(self.request.body)
        env = data['env']
        new_env = data['new_env']
        resp = self.env_manager.clone_env(env, new_env)
        if 'error' not in resp:
            status = 201  # CREATED

        # catch-all ok
        if 'error' in resp:
            status = 400

        self.set_status(status or 200)
        self.finish(json.dumps(resp))
