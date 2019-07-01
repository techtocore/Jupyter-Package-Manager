import json
import os
import re

from subprocess import Popen
from tempfile import TemporaryFile

from pkg_resources import parse_version
from notebook.base.handlers import (
    APIHandler,
    json_errors,
)
from tornado import web, escape

from .envmanager import EnvManager

from os.path import expanduser
home = expanduser("~")

def relativeDir(directory):
    if directory[0] != '/':
        directory = '/' + directory
    if directory[-1] != '/':
        directory = directory + '/'
    return home + directory


class EnvBaseHandler(APIHandler):
    """
    Maintains a reference to the
    'env_manager' which implements all of the conda functions.
    """
    @property
    def env_manager(self):
        """Return our env_manager instance"""
        return self.settings['env_manager']

# -----------------------------------------------------------------------------
# Package Management APIs
# -----------------------------------------------------------------------------


class PkgHandler(EnvBaseHandler):

    def clean(self, packages):
        # no hyphens up front, please
        _pkg_regex = r"(?P<pkg>[^\-][\-\da-zA-Z\._]+)"
        # don't allow arbitrary switches
        packages = [pkg for pkg in packages if re.match(_pkg_regex, pkg)]
        return packages

    """
    Handler for `POST /packages` which installs all
    the selected packages in the specified environment.
    """

    @json_errors
    def post(self):
        data = escape.json_decode(self.request.body)
        directory = data.get('dir')
        directory = relativeDir(directory)
        packages = data.get('packages')
        packages = self.clean(packages)
        resp = self.env_manager.install_packages(directory, packages)
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
        directory = data.get('dir')
        directory = relativeDir(directory)
        packages = data.get('packages')
        packages = self.clean(packages)
        resp = self.env_manager.update_packages(directory, packages)
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
        directory = data.get('dir')
        directory = relativeDir(directory)
        packages = data.get('packages')
        packages = self.clean(packages)
        resp = self.env_manager.remove_packages(directory, packages)
        if resp.get("error"):
            self.set_status(500)
        self.finish(json.dumps(resp))


class CheckUpdatePkgHandler(EnvBaseHandler):

    """
    Handler for `GET /packages/check_update` which checks for updates of all
    the selected packages in the specified environment.
    """

    @json_errors
    def get(self):
        directory = self.get_argument('dir', "None")
        directory = relativeDir(directory)
        resp = self.env_manager.check_update(directory)
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
