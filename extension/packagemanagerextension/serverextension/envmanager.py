# pylint: disable=C0321

import json
import os
import re
import uuid
import yaml

from packaging.version import parse
from subprocess import check_output, CalledProcessError
from traitlets.config.configurable import LoggingConfigurable
from traitlets import Dict

# these are the types of environments that can be created
package_map = {
    'python2': 'python=2 ipykernel',
    'python3': 'python=3 ipykernel'
}

CONDA_EXE = os.environ.get("CONDA_EXE", "conda")  # type: str

# try to match lines of json
JSONISH_RE = r'(^\s*["\{\}\[\],\d])|(["\}\}\[\],\d]\s*$)'


class EnvManager(LoggingConfigurable):
    '''
    This class defines all the actions done by conda
    '''

    def list_envs(self):
        '''
        List all environments associated with SWAN projects
        '''
        info = self._clean_conda_json(
            self._conda_execute('info --json'))

        def get_info(env):
            return {
                'name': os.path.basename(env),
                'dir': env
            }

        return [get_info(env) for env in info['envs'] if "swanproject" in env]

    def create_env(self, env, type):
        '''
        Creates a new conda env for asssociation with a SWAN project
        '''
        packages = package_map[type]
        output = self._conda_execute('create -y -q --json -n', env,
                                     *packages.split(" "))
        resp = self._clean_conda_json(output)

        return resp

    def delete_env(self, env):
        '''
        Removes the conda env completely
        '''
        output = self._conda_execute(
            'remove -y -q --all --json -n', env)

        return self._clean_conda_json(output)

    def install_packages(self, env, packages):
        '''
        Installs a list of packages onto an env
        '''
        output = self._conda_execute(
            'install -y -q --json -n', env, *packages)
        return self._clean_conda_json(output)

    def update_packages(self, env, packages):
        '''
        Updates package(s) in an env
        '''
        output = self._conda_execute(
            'update -y -q --json -n', env, *packages)
        return self._clean_conda_json(output)

    def remove_packages(self, env, packages):
        '''
        Removes a list of packages from an env
        '''
        output = self._conda_execute(
            'remove -y -q --json -n', env, *packages)
        return self._clean_conda_json(output)

    def list_packages(self, env):
        '''
        List the packages installed on an env
        '''
        packages = self._conda_execute('list --json -n', env)
        return self._clean_conda_json(packages)

    def export_env(self, env):
        '''
        Export the conda env specifiation as plain text
        '''
        return str(self._conda_execute('list -e -n', env))

    def check_update(self, env, packages):
        '''
        Checks for newer versions of packages in an env
        '''
        output = self._conda_execute('update --dry-run -q --json -n', env,
                                     *packages)
        return self._clean_conda_json(output)

    def package_search(self, q):
        '''
        This function lets users search for available packages that match a search query
        '''
        # this method is slow and operates synchronously
        output = self._conda_execute('search --json', q)
        data = self._clean_conda_json(output)

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

        return sorted(packages, key=lambda entry: entry.get("name"))

    def pkg_info(self, s):
        '''
        Abstracts unwanted details and normalizes the package JSON
        '''
        return {
            "build_string": s.get("build_string", s.get("build")),
            "name": s.get("name"),
            "version": s.get("version")
        }

    def _conda_execute(self, cmd, *args):
        '''
        Executes the conda command line
        '''
        cmd = CONDA_EXE + ' ' + cmd
        cmdline = cmd.split() + list(args)

        try:
            output = check_output(cmdline)
        except CalledProcessError as exc:
            output = exc.output

        return output.decode("utf-8")

    def _clean_conda_json(self, inputjson):
        '''
        Ensures that only valid JSONs are processed
        '''
        lines = inputjson.splitlines()

        try:
            return json.loads('\n'.join(lines))
        except Exception as err:
            raise Exception(err)

        # try to remove bad lines
        lines = [line for line in lines if re.match(JSONISH_RE, line)]

        try:
            cleanJson = json.loads('\n'.join(lines))
        except Exception as err:
            raise Exception(err)
        return cleanJson
