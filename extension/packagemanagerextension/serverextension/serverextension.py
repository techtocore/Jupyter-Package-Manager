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
from tornado import web

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


class MainEnvHandler(EnvBaseHandler):
    """
    Handler for `GET /environments` which lists the environments.
    """

    @json_errors
    def get(self):
        self.finish(json.dumps(self.env_manager.list_envs()))


class ExportEnvHandler(EnvBaseHandler):
    """
    Handler for `GET /environment_export/<name>` which
    exports the specified environment.
    """

    @json_errors
    def get(self, env):
        # export requirements file
        self.set_header('Content-Disposition',
                        'attachment; filename="%s"' % (env + '.txt'))
        self.finish(self.env_manager.export_env(env))


class CloneEnvHandler(EnvBaseHandler):
    """
    Handler for `POST /environment_clone` which
    exports the specified environment.
    """

    @json_errors
    def post(self):
        env = str(self.get_body_argument('env', default=None))
        new_env = str(self.get_body_argument('new_env', default=None))
        data = self.env_manager.clone_env(env, new_env)
        if 'error' not in data:
            status = 201  # CREATED

        # catch-all ok
        if 'error' in data:
            status = 400

        self.set_status(status or 200)
        self.finish(json.dumps(data))


class CreateEnvHandler(EnvBaseHandler):
    """
    Handler for `POST /environment_create` which
    exports the specified environment.
    """

    @json_errors
    def post(self):
        env = str(self.get_body_argument('env', default=None))
        env_type = self.get_argument('type', default=None)
        if env_type not in package_map:
            raise web.HTTPError(400)
        data = self.env_manager.create_env(env, env_type)
        if 'error' not in data:
            status = 201  # CREATED

        # catch-all ok
        if 'error' in data:
            status = 400

        self.set_status(status or 200)
        self.finish(json.dumps(data))


class DeleteEnvHandler(EnvBaseHandler):
    """
    Handler for `DELETE /environment_delete` which
    exports the specified environment.
    """

    @json_errors
    def delete(self):
        env = str(self.get_body_argument('env', default=None))
        data = self.env_manager.delete_env(env)

        # catch-all ok
        if 'error' in data:
            status = 400

        self.set_status(status or 200)
        self.finish(json.dumps(data))


# -----------------------------------------------------------------------------
# Package Management APIs
# -----------------------------------------------------------------------------


class ListPkgHandler(EnvBaseHandler):
    """
    Handler for `GET /list_packages/<name>` which lists
    the packages in the specified environment.
    """

    @json_errors
    def get(self, env):
        self.finish(json.dumps(self.env_manager.env_packages(env)))


class InstallPkgHandler(EnvBaseHandler):
    """
    Handler for `POST /install_packages` which lists
    the packages in the specified environment.
    """

    @json_errors
    def post(self):
        env = str(self.get_body_argument('env', default=None))
        packages = str(self.get_body_argument('packages', default=None))
        resp = self.env_manager.install_packages(env, packages)
        self.finish(json.dumps(resp))


class UpdatePkgHandler(EnvBaseHandler):
    """
    Handler for `PATCH /update_packages` which lists
    the packages in the specified environment.
    """

    @json_errors
    def patch(self):
        env = str(self.get_body_argument('env', default=None))
        packages = str(self.get_body_argument('packages', default=None))
        resp = self.env_manager.update_packages(env, packages)
        self.finish(json.dumps(resp))


class CheckUpdatePkgHandler(EnvBaseHandler):
    """
    Handler for `POST /check_update_packages` which lists
    the packages in the specified environment.
    """

    @json_errors
    def post(self):
        env = str(self.get_body_argument('env', default=None))
        packages = str(self.get_body_argument('packages', default=None))
        resp = self.env_manager.check_update(env, packages)
        self.finish(json.dumps(resp))


class DeletePkgHandler(EnvBaseHandler):
    """
    Handler for `DELETE /delete_packages` which lists
    the packages in the specified environment.
    """

    @json_errors
    def delete(self):
        env = str(self.get_body_argument('env', 'none'))
        packages = str(self.get_body_argument('packages', 'none'))
        resp = self.env_manager.remove_packages(env, packages)
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
    (r"/environments", MainEnvHandler),
    (r"/environment_export/%s" % _env_regex, ExportEnvHandler),
    (r"/environment_clone", CloneEnvHandler),
    (r"/environment_create", CreateEnvHandler),
    (r"/environment_delete", DeleteEnvHandler),
    (r"/list_packages/%s" % _env_regex, ListPkgHandler),
    (r"/install_packages", InstallPkgHandler),
    (r"/update_packages", UpdatePkgHandler),
    (r"/check_update_packages", CheckUpdatePkgHandler),
    (r"/delete_packages", DeleteEnvHandler),
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
    nbapp.log.info("Jupyter-Package-Manager: Handlers enabled")
