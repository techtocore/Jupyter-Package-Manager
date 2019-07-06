# pylint: disable=C0321

import os
import yaml

from traitlets.config.configurable import LoggingConfigurable

from .processhelper import ProcessHelper
process_helper = ProcessHelper()


class SwanProject(LoggingConfigurable):

    def __init__(self, directory):
        self.directory = directory
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
        packages = process_helper.conda_execute('list --json -n', env)
        packages = process_helper.clean_conda_json(packages)
        process_helper.update_yaml(env, packages, directory)

    def project_info(self):
        env = self.env
        directory = self.directory
        swandata = []
        directory = str(directory) + ".swanproject"
        try:
            packagesMD = yaml.load(open(directory))['PACKAGE_INFO']
        except:
            return {'error': "Can't find project info"}

        for item in packagesMD:
            swandata.append(process_helper.pkg_info(item))
            # details of all packages in the .swanproject file

        output = process_helper.conda_execute('list --json -n', env)
        data = process_helper.clean_conda_json(output)
        if 'error' in data:
            # we didn't get back a list of packages, we got a dictionary with
            # error info
            return data
        condadata = []
        for package in data:
            condadata.append(process_helper.pkg_info(package))
            # details of all packages in the corresponding env

        resp = {}
        resp['env'] = env
        '''
        Merge both the lists with the appropriate status of every package
        If in swanproj but not in conda -> alert the user to install
        if in conda but not in swanproj -> alert the user to sync the state (or do it automatically?)
        if in both -> keep calm and carry on
        '''
        resp['packages'] = process_helper.pkg_info_status(swandata, condadata)
        return resp

    def sync_packages(self):
        package_info = self.project_info()
        packages = []
        for i in package_info['packages']:
            if i['status'] != 'installed':
                packages.append(i['name'] + '=' + i['version'])
        return self.install_packages(packages)

    def export_env(self):
        env = self.env
        return str(process_helper.conda_execute('list -e -n', env))

    def check_update(self):
        env = self.env
        packagesJson = process_helper.conda_execute(
            'list --json -n', env)
        packagesJson = process_helper.clean_conda_json(packagesJson)
        packages = []
        for it in packagesJson:
            packages.append(it.get('name'))
        output = process_helper.conda_execute('update --dry-run -q --json -n', env,
                                              *packages)
        data = process_helper.clean_conda_json(output)

        if 'error' in data:
            # we didn't get back a list of packages, we got a dictionary with
            # error info
            return data
        elif 'actions' in data:
            links = data['actions'].get('LINK', [])
            package_versions = [link for link in links]
            return {
                "updates": [process_helper.pkg_info(pkg_version)
                            for pkg_version in package_versions]
            }
        else:
            # no action plan returned means everything is already up to date
            return {
                "updates": []
            }

    def install_packages(self, packages):
        env = self.env
        output = process_helper.conda_execute(
            'install -y -q --json -n', env, *packages)
        self.update_swanproject()
        return process_helper.clean_conda_json(output)

    def update_packages(self, packages):
        env = self.env
        output = process_helper.conda_execute(
            'update -y -q --json -n', env, *packages)
        self.update_swanproject()
        return process_helper.clean_conda_json(output)

    def remove_packages(self, packages):
        env = self.env
        output = process_helper.conda_execute(
            'remove -y -q --json -n', env, *packages)
        self.update_swanproject()
        return process_helper.clean_conda_json(output)
