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

# these are the types of environments that can be created
package_map = {
    'python2': 'python=2 ipykernel',
    'python3': 'python=3 ipykernel'
}

process_helper = ProcessHelper()


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
            env = process_helper.get_swanproject(directory)
        except:
            return {'error': "Can't find project"}
        output = process_helper.conda_execute(
            'remove -y -q --all --json -n', env)
        kdir = '.local/share/jupyter/kernels/' + env
        os.remove(kdir + '/kernel.json')
        os.rmdir(kdir)
        return process_helper.clean_conda_json(output)

    def project_info(self, directory):
        try:
            env = process_helper.get_swanproject(directory)
        except:
            return {'error': "Can't find project"}
        names = []
        packagesMD = {}
        directory = str(directory) + ".swanproject"
        try:
            packagesMD = yaml.load(open(directory))['PACKAGE_INFO']
        except:
            return {'error': "Can't find project info"}

        for item in packagesMD:
            names.append(item.get('name'))

        output = ProcessHelper.conda_execute('list --no-pip --json -n', env)
        data = ProcessHelper.clean_conda_json(output)
        if 'error' in data:
            # we didn't get back a list of packages, we got a dictionary with
            # error info
            return data

        return {
            "env": env,
            "packages": [ProcessHelper.pkg_info_status(package, names) for package in data]
        }

    def export_env(self, directory):
        try:
            env = process_helper.get_swanproject(directory)
        except:
            return {'error': "Can't find project"}
        return str(process_helper.conda_execute('list -e -n', env))

    def create_project(self, directory, type):
        name = uuid.uuid1()
        name = 'swanproject-' + str(name)
        data = {'ENV': name}

        folder = directory[:-1].split('/')[-1]

        if not os.path.exists(directory):
            # os.makedirs(directory)
            res = {'error': 'Project directory not available'}
            return res

        # if os.path.isfile(directory + '.swanproject'):
        #     res = {'error': 'This directory alreday contains a project'}
        #     return res

        packages = package_map[type]
        output = process_helper.conda_execute('create -y -q --json -n', name,
                                              *packages.split(" "))
        packages = process_helper.conda_execute(
            'list --no-pip --json -n', name)
        packages = process_helper.clean_conda_json(packages)
        op = process_helper.clean_conda_json(output)
        tp = json.dumps(op)
        js = json.loads(tp)
        kerneljson = {
            "argv": [js['prefix'] + "/bin/python",   "-m",
                     "ipykernel_launcher",
                     "-f",
                     "{connection_file}"],
            "display_name": "Python (" + folder + ")",
            "language": "python"
        }
        kdir = '.local/share/jupyter/kernels/' + name
        if not os.path.exists(kdir):
            os.makedirs(kdir)
        with open(kdir + '/kernel.json', 'w') as fp:
            json.dump(kerneljson, fp)

        data['PACKAGE_INFO'] = packages
        with open(directory + '.swanproject', 'w') as outfile:
            yaml.dump(data, outfile, default_flow_style=False)
        return op

    def check_update(self, directory):
        try:
            env = process_helper.get_swanproject(directory)
        except:
            return {'error': "Can't find project"}
        packagesJson = process_helper.conda_execute(
            'list --no-pip --json -n', env)
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
            env = process_helper.get_swanproject(directory)
        except:
            return {'error': "Can't find project"}
        output = process_helper.conda_execute(
            'install -y -q --json -n', env, *packages)
        data = {'ENV': env}
        packages = process_helper.conda_execute('list --no-pip --json -n', env)
        packages = process_helper.clean_conda_json(packages)
        data['PACKAGE_INFO'] = packages
        with open(directory, 'w') as outfile:
            yaml.dump(data, outfile, default_flow_style=False)
        return process_helper.clean_conda_json(output)

    def update_packages(self, directory, packages):
        try:
            env = process_helper.get_swanproject(directory)
        except:
            return {'error': "Can't find project"}
        output = process_helper.conda_execute(
            'update -y -q --json -n', env, *packages)
        data = {'ENV': env}
        packages = process_helper.conda_execute('list --no-pip --json -n', env)
        packages = process_helper.clean_conda_json(packages)
        data['PACKAGE_INFO'] = packages
        with open(directory, 'w') as outfile:
            yaml.dump(data, outfile, default_flow_style=False)
        return process_helper.clean_conda_json(output)

    def remove_packages(self, directory, packages):
        try:
            env = process_helper.get_swanproject(directory)
        except:
            return {'error': "Can't find project"}
        output = process_helper.conda_execute(
            'remove -y -q --json -n', env, *packages)
        data = {'ENV': env}
        packages = process_helper.conda_execute('list --no-pip --json -n', env)
        packages = process_helper.clean_conda_json(packages)
        data['PACKAGE_INFO'] = packages
        with open(directory, 'w') as outfile:
            yaml.dump(data, outfile, default_flow_style=False)
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
