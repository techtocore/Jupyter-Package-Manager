import json
import os
import re
import uuid

from subprocess import Popen
from tempfile import TemporaryFile

from pkg_resources import parse_version
from tornado import web, escape

from .envmanager import EnvManager, package_map
from .swanproject import SwanProject

env_manager = EnvManager()

class PackageManager():

# -----------------------------------------------------------------------------
# Project Management Modules
# -----------------------------------------------------------------------------

    def list_projects(self):

        '''
        Module for `GET /projects` which lists the projects.
        '''

        projects = {}
        projects['projects'] =  env_manager.list_envs()
        return projects

    def create_project(self, directory, env_type):

        '''
        Module for `POST /projects` which
        creates the specified environment.
        '''

        if env_type not in package_map:
            raise web.HTTPError(400)
        env = uuid.uuid1()
        env = 'swanproject-' + str(env)
        folder = directory[:-1].split('/')[-1]

        # if not os.path.exists(directory):
        #     raise Exception('Project directory not available')
        # try:
        #     swanproj = SwanProject(directory)
        #     resp = {'error': 'Project directory already associated with an env'}
        #     return res
        # except:
        #     pass

        try:
            resp = env_manager.create_env(env, folder, env_type)
            swanproj = SwanProject(directory, env)
            swanproj.update_swanproject()
        except Exception as e:
            resp = {'error': str(e)}
            
        return resp

    def delete_project(self, directory):

        '''
        Module for `DELETE /projects` which
        deletes the specified projects.
        '''
        
        # try:
        #     swanproj = SwanProject(directory)
        #     env = swanproj.env
        # except Exception as e:
        #     return {'error': str(e)}
        
        # # Clear the contents of the .swanproject file
        # open(directory + ".swanproject", 'w').close()

        try:
            dlist = []
            if type(directory) == type(dlist):
                for proj in directory:
                    resp = env_manager.delete_env(proj)
                    dlist.append(resp)
                resp = {'response': dlist}
            else:
                resp = env_manager.delete_env(directory)
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
            swanproj = SwanProject(directory)
            resp = swanproj.install_packages(packages)
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
            resp = swanproj.sync_packages()
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

    def install_packages(self, directory, packages):

        '''
        Module for `POST /packages` which installs all
        the selected packages in the specified environment.
        '''

        packages = self.clean(packages)
        try:
            swanproj = SwanProject(directory)
            resp = swanproj.install_packages(packages)
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
            resp = swanproj.update_packages(packages)
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
            resp = swanproj.remove_packages(packages)
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
            resp = swanproj.check_update()
        except Exception as e:
            resp = {'error': str(e)}
        return resp

    def export_package_text(self, directory):
        try:
            swanproj = SwanProject(directory)
            resp = swanproj.export_project()
        except Exception as e:
            resp = str(e)
        return resp
    
    def project_info(self, directory):
        try:
            swanproj = SwanProject(directory)
            resp = swanproj.project_info()
        except Exception as e:
            resp = {'error': str(e)}
        return resp

    def search(self, query):
        return env_manager.package_search(query)

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