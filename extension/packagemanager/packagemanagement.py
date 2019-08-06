import json
import os
import re
import uuid

from subprocess import Popen
from tempfile import TemporaryFile

from pkg_resources import parse_version
from tornado import web, escape

try:
    from .envmanager import EnvManager, package_map
    from .swanproject import SwanProject
except:
    from envmanager import EnvManager, package_map
    from swanproject import SwanProject

env_manager = EnvManager()


class PackageManager():
    '''
    This class contains all the logic of the server extension
    '''

# -----------------------------------------------------------------------------
# Project Management Modules
# -----------------------------------------------------------------------------

    def list_projects(self):
        '''
        Module for `GET /projects` which lists the projects.
        '''

        return env_manager.list_envs()

    def create_project(self, directory, env_type):
        '''
        Module for `POST /projects` which
        creates the specified environment.
        '''

        if env_type not in package_map:
            raise web.HTTPError(400)
        env = uuid.uuid1()
        env = 'swanproject-' + str(env)

        try:
            resp = env_manager.create_env(env, env_type)
            swanproj = SwanProject(directory)
            swanproj.env = env
            swanproj.packages = env_manager.list_packages(env)
            swanproj.update_yaml()
        except Exception as e:
            resp = {'error': str(e)}

        return resp

    def delete_project(self, directories):
        '''
        Module for `DELETE /projects` which
        deletes the specified projects.
        '''

        try:
            dlist = []
            for projectdir in directories:
                swanproject = SwanProject(projectdir)
                env = swanproject.env
                resp = env_manager.delete_env(env)
                dlist.append(resp)
                swanproject.clear_yaml()
            resp = {'response': dlist}
        except Exception as e:
            resp = {'error': str(e)}

        return resp

    def import_project(self, file1, directory):
        '''
        Module for `PUT /project_info` which
        updates a project with all the packages obtained from an export file
        '''

        tmp = file1['body'].splitlines()
        packages = []
        for i in tmp:
            if i[0] != '#':
                packages.append(i)
        try:
            self.install_packages(directory, packages)
        except Exception as e:
            resp = {'error': str(e)}

        return resp

    def sync_project(self, directory):
        '''
        Module for `PATCH /project_info` which
        syncs a .swanproject file and the corresponding conda env
        '''

        try:
            swanproj = SwanProject(directory)
            package_info = self.project_info_aux(swanproj)
            packages = []
            for i in package_info['packages']:
                if i['status'] != 'installed':
                    packages.append(i['name'] + '=' + i['version'])
            resp = self._install_packages_aux(swanproj, packages)
        except Exception as e:
            resp = {'error': str(e)}

        return resp

    def clone_project(self, directory):
        '''
        Module for `POST /project_clone` which clones a project in a new location
        '''

        try:
            swanproj = SwanProject(directory)
            env = uuid.uuid1()
            env = 'swanproject-' + str(env)
            resp = env_manager.create_env(env, 'python3')
            swanproj.env = env
            swanproj.update_yaml()
        except Exception as e:
            resp = {'error': str(e)}

        return resp


# -----------------------------------------------------------------------------
# Package Management APIs
# -----------------------------------------------------------------------------

    def clean(self, packages):
        # no hyphens up front, please
        _pkg_regex = r"(?P<pkg>[^\-][\-\da-zA-Z\._]+)"
        # don't allow arbitrary switches
        packages = [pkg for pkg in packages if re.match(_pkg_regex, pkg)]
        return packages

    def _install_packages_aux(self, swanproj, packages):
        env = swanproj.env
        resp = env_manager.install_packages(env, packages)
        swanproj.packages = env_manager.list_packages(env)
        swanproj.update_yaml()
        return resp

    def install_packages(self, directory, packages):
        '''
        Module for `POST /packages` which installs all
        the selected packages in the specified environment.
        '''

        packages = self.clean(packages)
        try:
            swanproj = SwanProject(directory)
            resp = self._install_packages_aux(swanproj, packages)
        except Exception as e:
            resp = {'error': str(e)}
        return resp

    def update_packages(self, directory, packages):
        '''
        Module for `PATCH /packages` which updates all
        the selected packages in the specified environment.
        '''

        packages = self.clean(packages)
        try:
            swanproj = SwanProject(directory)
            env = swanproj.env
            resp = env_manager.update_packages(env, packages)
            swanproj.packages = env_manager.list_packages(env)
            swanproj.update_yaml()
        except Exception as e:
            resp = {'error': str(e)}
        return resp

    def delete_packages(self, directory, packages):
        '''
        Module for `DELETE /packages` which deletes all
        the selected packages in the specified environment.
        '''

        packages = self.clean(packages)
        try:
            swanproj = SwanProject(directory)
            env = swanproj.env
            resp = env_manager.remove_packages(env, packages)
            swanproj.packages = env_manager.list_packages(env)
            swanproj.update_yaml()
        except Exception as e:
            resp = {'error': str(e)}
        return resp

    def check_update(self, directory):
        '''
        Module for `GET /packages/check_update` which checks for updates of all
        the selected packages in the specified environment.
        '''

        try:
            swanproj = SwanProject(directory)
            env = swanproj.env
            packagesJson = swanproj.packages
            packages = []
            for it in packagesJson:
                packages.append(it.get('name'))
            data = env_manager.check_update(env, packages)
            if 'error' in data:
                # we didn't get back a list of packages, we got a dictionary with
                # error info
                resp = data
            elif 'actions' in data:
                links = data['actions'].get('LINK', [])
                package_versions = [link for link in links]
                resp = {
                    "updates": [env_manager.pkg_info(pkg_version)
                                for pkg_version in package_versions]
                }
            else:
                # no action plan returned means everything is already up to date
                resp = {
                    "updates": []
                }
        except Exception as e:
            resp = {'error': str(e)}
        return resp

    def export_package_text(self, directory):
        try:
            swanproj = SwanProject(directory)
            resp = env_manager.export_env(swanproj.env)
        except Exception as e:
            resp = str(e)
        return resp

    def project_info_aux(self, swanproj):
        swandata = []
        env = swanproj.env
        packages = swanproj.packages
        for item in packages:
            swandata.append(env_manager.pkg_info(item))
            # details of all packages in the .swanproject file

        data = env_manager.list_packages(env)
        if 'error' in data:
            # we didn't get back a list of packages, we got a dictionary with
            # error info
            return data
        condadata = []
        for package in data:
            condadata.append(env_manager.pkg_info(package))
            # details of all packages in the corresponding env

        resp = {}
        resp['env'] = env
        '''
        Merge both the lists with the appropriate status of every package
        If in swanproj but not in conda -> alert the user to install
        if in conda but not in swanproj -> alert the user to sync the state (or do it automatically?)
        if in both -> keep calm and carry on
        '''
        resp['packages'] = self.pkg_info_status(swandata, condadata)

        return resp

    def project_info(self, directory):
        try:
            swanproj = SwanProject(directory)
            resp = self.project_info_aux(swanproj)
        except Exception as e:
            resp = {'error': str(e)}
        return resp

    def search(self, query):
        return env_manager.package_search(query)

    def pkg_info_status(self, swandata, condadata):
        '''
        Combines the data available in both the lists and determines the status of each package
        '''
        packages = {x['name']: x for x in swandata + condadata}.values()
        for i in packages:
            if i in swandata and i in condadata:
                i['status'] = 'installed'
            elif i in swandata and i not in condadata:
                i['status'] = 'not installed'
            elif i not in swandata and i in condadata:
                i['status'] = 'not synced'
        return list(packages)


class CondaSearcher(object):

    def __init__(self):
        '''
        Helper object that runs `conda search` to retrieve the
        list of packages available in the current conda channels.
        '''

        self.conda_process = None
        self.conda_temp = None

    def list_available(self, Module=None):
        '''
        List the available conda packages by kicking off a background
        conda process. Will return None. Call again to poll the process
        status. When the process completes, a list of packages will be
        returned upon success. On failure, the results of `conda search --json`
        will be returned (this will be a dict containing error information).
        '''

        self.log = Module.log

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
