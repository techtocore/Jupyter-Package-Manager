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
            raise Exception('Project directory not available')
        try:
            swanproj = SwanProject(directory)
            res = {'error': 'Project directory already associated with an env'}
            return res
        except:
            pass

        packages = package_map[type]
        output = process_helper.conda_execute('create -y -q --json -n', env,
                                              *packages.split(" "))
        resp = process_helper.clean_conda_json(output)

        swanproj = SwanProject(directory, env)
        swanproj.update_swanproject()

        return resp

    def delete_project(self, directory):
        try:
            swanproj = SwanProject(directory)
            env = swanproj.env
        except Exception as e:
            return {'error': str(e)}
        output = process_helper.conda_execute(
            'remove -y -q --all --json -n', env)
        # Clear the contents of the .swanproject file
        open(directory + ".swanproject", 'w').close()
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
