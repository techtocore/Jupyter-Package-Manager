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


static = os.path.join(os.path.dirname(__file__), 'static')

NS = r'api/packagemanager'


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
# ENV Management APIs
# -----------------------------------------------------------------------------


class ManageEnvHandler(EnvBaseHandler):

    """
    Handler for `GET /environments` which lists the environments.
    """

    @json_errors
    def get(self):
        self.finish(json.dumps(self.env_manager.list_envs()))

    """
    Handler for `POST /environments` which
    creates the specified environment.
    """

    @json_errors
    def post(self):
        data = escape.json_decode(self.request.body)
        env = data['env']
        env_type = data['env_type']
        if env_type not in package_map:
            raise web.HTTPError(400)
        resp = self.env_manager.create_env(env, env_type)
        if 'error' not in resp:
            status = 201  # CREATED

        # catch-all ok
        if 'error' in resp:
            status = 400

        self.set_status(status or 200)
        self.finish(json.dumps(resp))

    """
    Handler for `DELETE /environments` which
    deletes the specified environment.
    """

    @json_errors
    def delete(self):
        data = escape.json_decode(self.request.body)
        env = data['env']
        resp = self.env_manager.delete_env(env)

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

        if self.request.headers['Content-Type'] == 'text/plain':
            # export requirements file
            self.set_header('Content-Disposition',
                            'attachment; filename="%s"' % (env + '.txt'))
            self.finish(self.env_manager.export_env(env))

        if self.request.headers['Content-Type'] == 'application/json':
            # send list of all packages
            self.finish(json.dumps(self.env_manager.env_packages(env)))


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


# -----------------------------------------------------------------------------
# Package Management APIs
# -----------------------------------------------------------------------------


class PkgHandler(EnvBaseHandler):

    """
    Handler for `POST /packages` which installs all
    the selected packages in the specified environment.
    """

    @json_errors
    def post(self):
        data = escape.json_decode(self.request.body)
        env = data['env']
        packages = data['packages']
        resp = self.env_manager.install_packages(env, packages)
        if resp.get("error"):
            self.set_status(500)
        self.finish(json.dumps(resp))

    """
    Handler for `PATCH /packages` which updates all
    the selected packages in the specified environment.
    """

    @json_errors
    def patch(self):
        data = escape.json_decode(self.request.body)
        env = data['env']
        packages = data['packages']
        resp = self.env_manager.update_packages(env, packages)
        if resp.get("error"):
            self.set_status(500)
        self.finish(json.dumps(resp))

    """
    Handler for `DELETE /packages` which deletes all
    the selected packages in the specified environment.
    """

    @json_errors
    def delete(self):
        data = escape.json_decode(self.request.body)
        env = data['env']
        packages = data['packages']
        resp = self.env_manager.remove_packages(env, packages)
        if resp.get("error"):
            self.set_status(500)
        self.finish(json.dumps(resp))


class CheckUpdatePkgHandler(EnvBaseHandler):

    """
    Handler for `POST /packages/check_update` which checks for updates of all
    the selected packages in the specified environment.
    """

    @json_errors
    def post(self):
        data = escape.json_decode(self.request.body)
        env = data['env']
        packages = data['packages']
        resp = self.env_manager.check_update(env, packages)
        if resp.get("error"):
            self.set_status(500)
        self.finish(json.dumps(resp))


class CondaSearcher(object):

    """
    Helper object that runs `conda search` to retrieve the
    list of packages available in the current conda channels.
    """

    def __init__(self):
        self.conda_process = None
        self.conda_temp = None

    def list_available(self, handler=None):

        """
        List the available conda packages by kicking off a background
        conda process. Will return None. Call again to poll the process
        status. When the process completes, a list of packages will be
        returned upon success. On failure, the results of `conda search --json`
        will be returned (this will be a dict containing error information).
        """

        self.log = handler.log

        if self.conda_process is not None:
            # already running, check for completion
            self.log.debug('Already running: pid %s', self.conda_process.pid)

            status = self.conda_process.poll()
            self.log.debug('Status %s', status)

            if status is not None:
                # completed, return the data
                self.log.debug('Done, reading output')
                self.conda_process = None

                self.conda_temp.seek(0)
                data = json.loads(self.conda_temp.read())
                self.conda_temp = None

                if 'error' in data:
                    # we didn't get back a list of packages, we got a
                    # dictionary with error info
                    return data

                packages = []

                for entries in data.values():
                    max_version = None
                    max_version_entry = None

                    for entry in entries:
                        version = parse_version(entry.get('version', ''))

                        if max_version is None or version > max_version:
                            max_version = version
                            max_version_entry = entry

                    packages.append(max_version_entry)

                return sorted(packages, key=lambda entry: entry.get('name'))

        else:
            # Spawn subprocess to get the data
            self.log.debug('Starting conda process')
            self.conda_temp = TemporaryFile(mode='w+')
            cmdline = 'conda search --json'.split()
            self.conda_process = Popen(cmdline, stdout=self.conda_temp,
                                       bufsize=4096)
            self.log.debug('Started: pid %s', self.conda_process.pid)

        return None


searcher = CondaSearcher()


class AvailablePackagesHandler(EnvBaseHandler):

    """
    Handler for `GET /packages/available`, which uses CondaSearcher
    to list the packages available for installation.
    """

    @json_errors
    def get(self):
        data = searcher.list_available(self)

        if data is None:
            # tell client to check back later
            self.clear()
            self.set_status(202)  # Accepted
            self.finish('{}')
        else:
            self.finish(json.dumps({"packages": data}))


class SearchHandler(EnvBaseHandler):
    
    """
    Handler for `GET /packages/search?q=<query>`, which uses CondaSearcher
    to search the available conda packages.
    """

    @json_errors
    def get(self):
        q = self.get_argument('q', "None")
        self.finish(json.dumps(self.env_manager.package_search(q)))


# -----------------------------------------------------------------------------
# URL to handler mappings
# -----------------------------------------------------------------------------


# there is almost no text that is invalid, but no hyphens up front, please
# neither all these suspicious but valid caracthers...
_env_regex = r"(?P<env>[^/&+$?@<>%*-][^/&+$?@<>%*]*)"

# no hyphens up front, please
_pkg_regex = r"(?P<pkg>[^\-][\-\da-zA-Z\._]+)"


default_handlers = [
    (r"/environments", ManageEnvHandler),
    (r"/environments/%s" % _env_regex, ExportEnvHandler),
    (r"/environment_clone", CloneEnvHandler),
    (r"/packages", PkgHandler),
    (r"/packages/check_update", CheckUpdatePkgHandler),
    (r"/packages/available", AvailablePackagesHandler),
    (r"/packages/search", SearchHandler),
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
