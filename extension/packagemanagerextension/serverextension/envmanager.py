# pylint: disable=C0321

import json
import os
import re
import uuid
import yaml

from packaging.version import parse

from traitlets.config.configurable import LoggingConfigurable
from traitlets import Dict

from .processhelper import ProcessHelper
from .swanproject import SwanProject

# these are the types of environments that can be created
package_map = {
    'python2': 'python=2 ipykernel',
    'python3': 'python=3 ipykernel'
}

process_helper = ProcessHelper()
swan_project = SwanProject()


class EnvManager(LoggingConfigurable):

    envs = Dict()

    def list_projects(self):
        """List all projects that conda knows about"""
        info = process_helper.clean_conda_json(
            process_helper.conda_execute('info --json'))

        def get_info(env):
            return {
                'name': os.path.basename(env),
                'dir': env
            }

        return {
            "projects": [get_info(env) for env in info['envs'] if "swanproject" in env]
        }

    def delete_project(self, directory):
        try:
            env = swan_project.get_swanproject(directory)
        except:
            return {'error': "Can't find project"}
        output = process_helper.conda_execute(
            'remove -y -q --all --json -n', env)
        '''
        The corresponding kernel.json file needs to be removed to ensure that only valid kernels
        are shown to the user.
        '''
        kdir = '.local/share/jupyter/kernels/' + env
        os.remove(kdir + '/kernel.json')
        os.rmdir(kdir)
        return process_helper.clean_conda_json(output)

    def project_info(self, directory):
        try:
            env = swan_project.get_swanproject(directory)
        except:
            return {'error': "Can't find project"}
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

    def sync_packages(self, directory):
        package_info = self.project_info(directory)
        packages = []
        for i in package_info['packages']:
            if i['status'] != 'installed':
                packages.append(i['name'] + '=' + i['version'])
        return self.install_packages(directory, packages)

    def export_env(self, directory):
        try:
            env = swan_project.get_swanproject(directory)
        except:
            return {'error': "Can't find project"}
        return str(process_helper.conda_execute('list -e -n', env))

    def create_project(self, directory, type):
        env = uuid.uuid1()
        env = 'swanproject-' + str(env)

        folder = directory[:-1].split('/')[-1]

        if not os.path.exists(directory):
            res = {'error': 'Project directory not available'}
            return res

        packages = package_map[type]
        output = process_helper.conda_execute('create -y -q --json -n', env,
                                              *packages.split(" "))
        resp = process_helper.clean_conda_json(output)

        temp = json.dumps(resp)
        returnDict = json.loads(temp)
        kerneljson = {
            "argv": [returnDict['prefix'] + "/bin/python",   "-m",
                     "ipykernel_launcher",
                     "-f",
                     "{connection_file}"],
            "display_name": "Python (" + folder + ")",
            "language": "python"
        }
        kdir = '.local/share/jupyter/kernels/' + env

        '''
        The kernel.json file is used by jupyter to recognize the iPython kernels (belonging to different env). 
        It is needed to list down the kernel from the newly created environment corresponding to the project.
        '''

        if not os.path.exists(kdir):
            os.makedirs(kdir)
        with open(kdir + '/kernel.json', 'w') as fp:
            json.dump(kerneljson, fp)

        swan_project.update_swanproject(env)
        return resp

    def check_update(self, directory):
        try:
            env = swan_project.get_swanproject(directory)
        except:
            return {'error': "Can't find project"}
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

    def install_packages(self, directory, packages):
        try:
            env = swan_project.get_swanproject(directory)
        except:
            return {'error': "Can't find project"}
        output = process_helper.conda_execute(
            'install -y -q --json -n', env, *packages)
        swan_project.update_swanproject(directory)
        return process_helper.clean_conda_json(output)

    def update_packages(self, directory, packages):
        try:
            env = swan_project.get_swanproject(directory)
        except:
            return {'error': "Can't find project"}
        output = process_helper.conda_execute(
            'update -y -q --json -n', env, *packages)
        swan_project.update_swanproject(directory)
        return process_helper.clean_conda_json(output)

    def remove_packages(self, directory, packages):
        try:
            env = swan_project.get_swanproject(directory)
        except:
            return {'error': "Can't find project"}
        output = process_helper.conda_execute(
            'remove -y -q --json -n', env, *packages)
        swan_project.update_swanproject(directory)
        return process_helper.clean_conda_json(output)

    def package_search(self, q):
        # this method is slow and operates synchronously
        output = process_helper.conda_execute('search --json', q)
        data = process_helper.clean_conda_json(output)

        if 'error' in data:
            # we didn't get back a list of packages, we got a dictionary with
            # error info
            return data

        packages = []

        for entries in data.values():
            max_version = None
            max_version_entry = None

            for entry in entries:
                version = parse(entry.get("version", ""))

                if max_version is None or version > max_version:
                    max_version = version
                    max_version_entry = entry

            packages.append(max_version_entry)

        return {"packages": sorted(packages, key=lambda entry: entry.get("name"))}
