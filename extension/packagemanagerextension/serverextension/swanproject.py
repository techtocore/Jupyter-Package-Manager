# pylint: disable=C0321

import os
import yaml

from traitlets.config.configurable import LoggingConfigurable
from os.path import expanduser
from .envmanager import EnvManager

env_manager = EnvManager()

class SwanProject(LoggingConfigurable):

    def __init__(self, directory, *args):
        self.directory = self.relativeDir(directory)
        if len(args) > 0:
            self.env = args[0]
        else:
            self.env = self.get_swanproject()

    def get_swanproject(self):
        '''
        Directory to env mapping
        '''
        directory = self.directory
        directory = directory + ".swanproject"
        try:
            env = yaml.load(open(directory))['ENV']
        except:
            raise Exception("Can't find project")
        return env

    def update_swanproject(self):
        '''
        Update the .swanproject file with the updated metadata
        '''
        directory = self.directory
        env = self.env
        packages = env_manager.list_packages(env)
        self.update_yaml(env, packages, directory)

    def project_info(self):
        env = self.env
        directory = self.directory
        swandata = []
        directory = str(directory) + ".swanproject"
        try:
            packagesMD = yaml.load(open(directory))['PACKAGE_INFO']
        except:
            raise Exception("Can't find project info")

        for item in packagesMD:
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

    def sync_packages(self):
        package_info = self.project_info()
        packages = []
        for i in package_info['packages']:
            if i['status'] != 'installed':
                packages.append(i['name'] + '=' + i['version'])
        return self.install_packages(packages)

    def export_project(self):
        env = self.env
        return env_manager.export_env(env)

    def check_update(self):
        env = self.env
        packagesJson = env_manager.list_packages(env)
        packages = []
        for it in packagesJson:
            packages.append(it.get('name'))
        data = env_manager.check_update(env, packages)
        if 'error' in data:
            # we didn't get back a list of packages, we got a dictionary with
            # error info
            return data
        elif 'actions' in data:
            links = data['actions'].get('LINK', [])
            package_versions = [link for link in links]
            return {
                "updates": [env_manager.pkg_info(pkg_version)
                            for pkg_version in package_versions]
            }
        else:
            # no action plan returned means everything is already up to date
            return {
                "updates": []
            }

    def install_packages(self, packages):
        env = self.env
        output = env_manager.install_packages(env, packages)
        self.update_swanproject()
        return output

    def update_packages(self, packages):
        env = self.env
        output = env_manager.update_packages(env, packages)
        self.update_swanproject()
        return output

    def remove_packages(self, packages):
        env = self.env
        output = env_manager.remove_packages(env, packages)
        self.update_swanproject()
        return output

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
        return packages

    def update_yaml(self, name, packages, directory):
        '''
        Updates the .swanproject file with new metadata
        '''
        directory = directory + ".swanproject"
        data = {'ENV': name}
        data['PACKAGE_INFO'] = packages
        try:
            with open(directory, 'w') as outfile:
                yaml.dump(data, outfile, default_flow_style=False)
        except:
            raise Exception("Can't update .swanproject file")

    def relativeDir(self, directory):
        '''
        Ensures that all directories are relative to home
        '''
        home = expanduser("~")
        if directory[0] != '/':
            directory = '/' + directory
        if directory[-1] != '/':
            directory = directory + '/'
        return home + directory
