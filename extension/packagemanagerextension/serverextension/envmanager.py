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


class EnvManager(LoggingConfigurable):

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

        swanproj = SwanProject(directory)
        swanproj.update_swanproject()

        return resp

    def delete_project(self, directory):
        swanproj = SwanProject(directory)
        env = swanproj.env
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
